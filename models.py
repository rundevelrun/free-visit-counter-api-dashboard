from app import db
import datetime

class Site(db.Model):
    __tablename__ = 'sites'
    
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(255), unique=True, nullable=False)
    total_count = db.Column(db.Integer, default=0)
    today_count = db.Column(db.Integer, default=0)
    today_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    visits = db.relationship('VisitLog', backref='site', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Site {self.domain}>'

class VisitLog(db.Model):
    __tablename__ = 'visit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id', ondelete='CASCADE'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    timezone = db.Column(db.String(50), default='UTC')
    page_path = db.Column(db.String(255), nullable=True)
    page_title = db.Column(db.String(255), nullable=True)
    referrer = db.Column(db.String(255), nullable=True)
    search_query = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return f'<VisitLog {self.id} for site {self.site_id}>'
