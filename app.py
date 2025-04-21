from flask import Flask, request, jsonify, render_template, redirect, url_for, g, session
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, gettext
from flask_migrate import Migrate
import redis
import os
import datetime
import json
from dotenv import load_dotenv
import hashlib
import pytz
from sqlalchemy import func

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Babel configuration
def get_locale():
    # Get locale from URL parameter, user settings, or request headers
    locale = request.args.get('lang')
    if locale:
        session['lang'] = locale
    return session.get('lang', request.accept_languages.best_match(['en', 'ko', 'ja']))

babel = Babel(app, locale_selector=get_locale)

# Initialize Redis
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    password=os.getenv('REDIS_PASSWORD', None),
    db=int(os.getenv('REDIS_DB', 0))
)

# Import models after initializing db
from models import Site, VisitLog

# Context processor for translations and custom filters
@app.context_processor
def utility_processor():
    def translate(text):
        return gettext(text)

    def now(tz='utc', fmt='%Y'):
        from datetime import datetime
        import pytz

        timezone = pytz.timezone(tz)
        return datetime.now(timezone).strftime(fmt)

    return dict(_=translate, now=now)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api-docs')
def api_docs():
    return render_template('api-docs.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/installation')
def installation():
    return render_template('installation.html')

@app.route('/dashboard')
def dashboard():
    domain = request.args.get('domain')
    if not domain:
        return redirect(url_for('login'))

    # Get site data
    site = Site.query.filter_by(domain=domain).first()
    if not site:
        return redirect(url_for('not_found'))

    # Get current date and calculate date ranges
    now = datetime.datetime.now()
    today = now.date()
    yesterday = today - datetime.timedelta(days=1)

    # Current week
    week_start = today - datetime.timedelta(days=today.weekday())
    week_end = week_start + datetime.timedelta(days=6)

    # Previous week
    prev_week_start = week_start - datetime.timedelta(days=7)
    prev_week_end = week_start - datetime.timedelta(days=1)

    # Current month
    month_start = today.replace(day=1)
    next_month = today.replace(day=28) + datetime.timedelta(days=4)
    month_end = next_month.replace(day=1) - datetime.timedelta(days=1)

    # Previous month
    last_month = month_start - datetime.timedelta(days=1)
    prev_month_start = last_month.replace(day=1)
    prev_month_end = month_start - datetime.timedelta(days=1)

    # Current year
    year_start = today.replace(month=1, day=1)
    year_end = today.replace(month=12, day=31)

    # Previous year
    prev_year_start = year_start.replace(year=year_start.year-1)
    prev_year_end = year_end.replace(year=year_end.year-1)

    # Query for today's visits
    today_visits = db.session.query(
        func.count(VisitLog.id)
    ).filter(
        VisitLog.site_id == site.id,
        func.date(VisitLog.timestamp) == today
    ).scalar() or 0

    # Fix for Today count showing 5 when it should be 0
    if today_visits == 0:
        site.today_count = 0
        db.session.commit()

    # Query for yesterday's visits
    yesterday_visits = db.session.query(
        func.count(VisitLog.id)
    ).filter(
        VisitLog.site_id == site.id,
        func.date(VisitLog.timestamp) == yesterday
    ).scalar() or 0

    # Calculate today's change percentage
    if yesterday_visits > 0:
        today_change = int(((today_visits - yesterday_visits) / yesterday_visits) * 100)
    else:
        today_change = 100 if today_visits > 0 else 0

    # Query for current week's visits
    week_visits = db.session.query(
        func.date(VisitLog.timestamp).label('date'),
        func.count(VisitLog.id).label('count')
    ).filter(
        VisitLog.site_id == site.id,
        func.date(VisitLog.timestamp) >= week_start,
        func.date(VisitLog.timestamp) <= week_end
    ).group_by(
        func.date(VisitLog.timestamp)
    ).all()

    # Create a dictionary with dates and counts for the week
    week_data = {(week_start + datetime.timedelta(days=i)).strftime('%a'): 0 for i in range(7)}
    for date, count in week_visits:
        day_name = date.strftime('%a')
        week_data[day_name] = count

    # Calculate week total
    week_total = sum(week_data.values())

    # Query for previous week's visits
    prev_week_total = db.session.query(
        func.count(VisitLog.id)
    ).filter(
        VisitLog.site_id == site.id,
        func.date(VisitLog.timestamp) >= prev_week_start,
        func.date(VisitLog.timestamp) <= prev_week_end
    ).scalar() or 0

    # Calculate week change percentage
    if prev_week_total > 0:
        week_change = int(((week_total - prev_week_total) / prev_week_total) * 100)
    else:
        week_change = 100 if week_total > 0 else 0

    # Query for current month's visits
    month_visits = db.session.query(
        func.date(VisitLog.timestamp).label('date'),
        func.count(VisitLog.id).label('count')
    ).filter(
        VisitLog.site_id == site.id,
        func.date(VisitLog.timestamp) >= month_start,
        func.date(VisitLog.timestamp) <= month_end
    ).group_by(
        func.date(VisitLog.timestamp)
    ).all()

    # Create a dictionary with dates and counts for the month
    days_in_month = (month_end - month_start).days + 1
    month_data = {str(i+1): 0 for i in range(days_in_month)}
    for date, count in month_visits:
        day = str(date.day)
        month_data[day] = count

    # Calculate month total
    month_total = sum(month_data.values())

    # Query for previous month's visits
    prev_month_total = db.session.query(
        func.count(VisitLog.id)
    ).filter(
        VisitLog.site_id == site.id,
        func.date(VisitLog.timestamp) >= prev_month_start,
        func.date(VisitLog.timestamp) <= prev_month_end
    ).scalar() or 0

    # Calculate month change percentage
    if prev_month_total > 0:
        month_change = int(((month_total - prev_month_total) / prev_month_total) * 100)
    else:
        month_change = 100 if month_total > 0 else 0

    # Calculate today's hourly visits (0~23)
    today_data = [0] * 24
    hourly_visits = db.session.query(
        func.extract('hour', VisitLog.timestamp).label('hour'),
        func.count(VisitLog.id)
    ).filter(
        VisitLog.site_id == site.id,
        func.date(VisitLog.timestamp) == today
    ).group_by('hour').all()

    for hour, count in hourly_visits:
        today_data[int(hour)] = count

    # Calculate current year's monthly visits
    year_data = [0] * 12
    this_year = today.year
    monthly_visits = db.session.query(
        func.extract('month', VisitLog.timestamp).label('month'),
        func.count(VisitLog.id)
    ).filter(
        VisitLog.site_id == site.id,
        func.extract('year', VisitLog.timestamp) == this_year
    ).group_by('month').all()

    for month, count in monthly_visits:
        year_data[int(month) - 1] = count

    # Calculate all time visits by year
    all_data = {}
    yearly_visits = db.session.query(
        func.extract('year', VisitLog.timestamp).label('year'),
        func.count(VisitLog.id)
    ).filter(
        VisitLog.site_id == site.id
    ).group_by('year').all()

    for year, count in yearly_visits:
        all_data[int(year)] = count

    # Get popular posts for different time periods
    popular_posts_week = get_popular_posts(site.id, week_start, week_end)
    popular_posts_month = get_popular_posts(site.id, month_start, month_end)
    popular_posts_year = get_popular_posts(site.id, year_start, year_end)
    popular_posts_all = get_popular_posts(site.id)

    # Get referrer statistics for different time periods
    referrers_week = get_referrers(site.id, week_start, week_end)
    referrers_month = get_referrers(site.id, month_start, month_end)
    referrers_year = get_referrers(site.id, year_start, year_end)
    referrers_all = get_referrers(site.id)

    # Get recent posts
    recent_posts = get_recent_posts(site.id)
        
    return render_template('dashboard.html',
                           site=site,
                           week_data=week_data,
                           month_data=month_data,
                           year_data=year_data,
                           all_data=all_data,
                           today_data=today_data,
                           week_total=week_total,
                           month_total=month_total,
                           today_visits=today_visits,
                           today_change=today_change,
                           week_change=week_change,
                           month_change=month_change,
                           popular_posts_week=popular_posts_week,
                           popular_posts_month=popular_posts_month,
                           popular_posts_year=popular_posts_year,
                           popular_posts_all=popular_posts_all,
                           referrers_week=referrers_week,
                           referrers_month=referrers_month,
                           referrers_year=referrers_year,
                           referrers_all=referrers_all,
                           recent_posts=recent_posts
                           )

@app.route('/not-found')
def not_found():
    return render_template('not-found.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error=404), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error=500), 500

# API Routes
@app.route('/visit', methods=['POST'])
def record_visit():
    try:
        data = request.get_json()

        if not data or 'domain' not in data:
            return jsonify({'error': 'Invalid request data'}), 400

        domain = data.get('domain')
        timezone = data.get('timezone', 'UTC')
        page_path = data.get('page_path', '')
        page_title = data.get('page_title', '')
        referrer = data.get('referrer', '')
        search_query = data.get('search_query', '')

        # Get or create site
        site = Site.query.filter_by(domain=domain).first()
        if not site:
            site = Site(domain=domain)
            db.session.add(site)
            db.session.commit()

        # Generate visitor ID based on IP and user agent
        visitor_id = hashlib.md5(
            f"{request.remote_addr}:{request.headers.get('User-Agent')}".encode()
        ).hexdigest()

        # Check if this visitor has been counted recently
        visitor_key = f"visitor:{site.id}:{visitor_id}"
        if not redis_client.exists(visitor_key):
            # Record the visit
            visit_log = VisitLog(
                site_id=site.id, 
                timezone=timezone,
                page_path=page_path,
                page_title=page_title,
                referrer=referrer,
                search_query=search_query
            )
            db.session.add(visit_log)
            db.session.commit()

            # Set TTL for 20 minutes to prevent duplicate counting
            redis_client.setex(visitor_key, 1200, 1)

            # Update site counts
            site.total_count += 1

            # Calculate today's date in visitor's timezone
            try:
                tz = pytz.timezone(timezone)
                visitor_now = datetime.datetime.now(tz)
                visitor_today = visitor_now.date()

                # If the site's today_date is different from visitor's today,
                # reset the today_count
                if not site.today_date or site.today_date != visitor_today:
                    site.today_date = visitor_today
                    site.today_count = 1
                else:
                    site.today_count += 1

                db.session.commit()
            except pytz.exceptions.UnknownTimeZoneError:
                # Fallback to UTC if timezone is invalid
                site.today_count += 1
                db.session.commit()

        return jsonify({
            "dashboardUrl": f"https://visitor.6developer.com/dashboard?domain={site.domain}",
            "totalCount": site.total_count,
            "todayCount": site.today_count
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/visit', methods=['GET'])
def get_visit_stats():
    domain = request.args.get('domain')

    if not domain:
        return jsonify({
            "dashboardUrl": "https://visitor.6developer.com/dashboard?domain=",
            "totalCount": 0,
            "todayCount": 0
        })

    site = Site.query.filter_by(domain=domain).first()

    if not site:
        return jsonify({
            "dashboardUrl": f"https://visitor.6developer.com/dashboard?domain={domain}",
            "totalCount": 0,
            "todayCount": 0
        })

    # Get today's visit count based on timezone
    try:
        from datetime import datetime
        tz = pytz.timezone(site.timezone or 'UTC')
        now = datetime.now(tz)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        today_count = VisitLog.query.filter(
            VisitLog.site_id == site.id,
            VisitLog.timestamp >= start_of_day,
            VisitLog.timestamp <= end_of_day
        ).count()
    except Exception:
        today_count = site.today_count

    return jsonify({
        "dashboardUrl": f"https://visitor.6developer.com/dashboard?domain={site.domain}",
        "totalCount": site.total_count,
        "todayCount": today_count
    })

def get_popular_posts(site_id, start_date=None, end_date=None, limit=10):
    """Get popular posts for a site within a date range."""
    query = db.session.query(
        VisitLog.page_path,
        VisitLog.page_title,
        func.count(VisitLog.id).label('visit_count')
    ).filter(
        VisitLog.site_id == site_id,
        VisitLog.page_path != ''
    )
    
    if start_date:
        query = query.filter(func.date(VisitLog.timestamp) >= start_date)
    if end_date:
        query = query.filter(func.date(VisitLog.timestamp) <= end_date)
    
    return query.group_by(
        VisitLog.page_path,
        VisitLog.page_title
    ).order_by(
        func.count(VisitLog.id).desc()
    ).limit(limit).all()

def get_referrers(site_id, start_date=None, end_date=None, limit=10):
    """Get referrer statistics for a site within a date range."""
    query = db.session.query(
        VisitLog.referrer,
        func.count(VisitLog.id).label('visit_count')
    ).filter(
        VisitLog.site_id == site_id,
        VisitLog.referrer != ''
    )
    
    if start_date:
        query = query.filter(func.date(VisitLog.timestamp) >= start_date)
    if end_date:
        query = query.filter(func.date(VisitLog.timestamp) <= end_date)
    
    return query.group_by(
        VisitLog.referrer
    ).order_by(
        func.count(VisitLog.id).desc()
    ).limit(limit).all()

def get_recent_posts(site_id, limit=10):
    """Get recent posts for a site."""
    return db.session.query(
        VisitLog.page_path,
        VisitLog.page_title,
        VisitLog.referrer,
        VisitLog.search_query,
        VisitLog.timestamp
    ).filter(
        VisitLog.site_id == site_id,
        VisitLog.page_path != ''
    ).order_by(
        VisitLog.timestamp.desc()
    ).limit(limit).all()
