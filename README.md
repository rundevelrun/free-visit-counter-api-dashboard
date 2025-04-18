# Visitor Counter

A lightweight visitor counter for websites with a beautiful dashboard and API.

![Visitor Counter Dashboard](https://via.placeholder.com/800x400?text=Visitor+Counter+Dashboard)

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [NPM Package](#npm-package)
- [API Documentation](#api-documentation)
- [Installation](#installation)
- [Deployment](#deployment)
- [Configuration](#configuration)
- [Multilingual Support](#multilingual-support)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Real-time Tracking**: Track visitors in real-time with accurate counting and duplicate prevention
- **Responsive Dashboard**: View your visitor statistics on any device with our responsive dashboard
- **Easy Integration**: Simple API makes it easy to integrate with any website or application
- **Multiple Websites**: Track visitors across multiple domains with a single account
- **Multilingual Support**: Available in English, Korean, and Japanese
- **Dark/Light Theme**: Switch between dark and light themes for comfortable viewing
- **Duplicate Prevention**: Uses Redis with a 20-minute TTL to avoid counting the same visitor multiple times
- **Timezone Support**: Calculates "today" based on the visitor's timezone
- **NPM Package**: Official NPM package for easy integration with JavaScript frameworks

## 🚀 Quick Start

### 1. Add this script to your website

<code-block language="html">
<script>
(function() {
  const domain = encodeURIComponent(window.location.hostname);
  const timezone = encodeURIComponent(Intl.DateTimeFormat().resolvedOptions().timeZone);
  
  fetch('https://visitor.6developer.com/visit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ domain, timezone })
  })
  .then(response => response.json())
  .then(data => {
    console.log('Visitor count:', data);
    // You can display the count on your page
    if (document.getElementById('visitor-count')) {
      document.getElementById('visitor-count').textContent = data.totalCount;
    }
  })
  .catch(error => console.error('Error:', error));
})();
</script>
</code-block>

### 2. View your dashboard

Go to `https://visitor.6developer.com/login` and enter your domain to see your visitor statistics.

## 📦 NPM Package

Use our official NPM package for easy integration with JavaScript frameworks:

<code-block language="bash">
npm install @rundevelrun/free-visitor-counter
</code-block>

### Usage with React

<code-block language="jsx">
import { VisitorCounter } from '@rundevelrun/free-visitor-counter';

function App() {
  return (
    <div>
      <h1>My Website</h1>
      <VisitorCounter />
    </div>
  );
}
</code-block>

### Usage with JavaScript

<code-block language="javascript">
import { trackVisit, displayCounter } from '@rundevelrun/free-visitor-counter';

// Track visit
trackVisit().then(data => {
  console.log('Visitor count:', data);
});

// Display counter in element with id "visitor-counter"
displayCounter('visitor-counter');
</code-block>

For more information, visit the [GitHub repository](https://github.com/rundevelrun/free-visitor-counter).

## 📊 API Documentation

### Base URL

<code-block>
https://visitor.6developer.com
</code-block>

### Record a Visit

<code-block>
POST /visit
</code-block>

**Request Body:**

<code-block language="json">
{
  "domain": "example.com",
  "timezone": "America/New_York" // Optional, defaults to UTC
}
</code-block>

**Response:**

<code-block language="json">
{
  "dashboardUrl": "https://visitor.6developer.com/dashboard?domain=example.com",
  "totalCount": 42,
  "todayCount": 5
}
</code-block>

### Get Visit Statistics

<code-block>
GET /visit?domain=example.com
</code-block>

**Response:**

<code-block language="json">
{
  "dashboardUrl": "https://visitor.6developer.com/dashboard?domain=example.com",
  "totalCount": 42,
  "todayCount": 5
}
</code-block>

For more details, see the [API Documentation](https://visitor.6developer.com/api-docs).

## 🛠️ Installation

### Prerequisites

- Python 3.9+
- PostgreSQL
- Redis

### Setup

1. Clone the repository

<code-block language="bash">
git clone https://github.com/rundevelrun/visitor-counter.git
cd visitor-counter
</code-block>

2. Create a virtual environment

<code-block language="bash">
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
</code-block>

3. Install dependencies

<code-block language="bash">
pip install -r requirements.txt
</code-block>

4. Set up environment variables

Create a `.env` file in the project root:

<code-block>
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://username:password@localhost/visitor_counter
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
</code-block>

5. Initialize the database

<code-block language="bash">
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
</code-block>

6. Run the application

<code-block language="bash">
flask run
</code-block>

## 🚀 Deployment

### Deploying to a VPS

1. Set up a Python environment on your server
2. Install PostgreSQL and Redis
3. Clone the repository and follow the setup steps
4. Set up a production WSGI server (Gunicorn, uWSGI)
5. Configure Nginx as a reverse proxy

Example Nginx configuration:

<code-block language="nginx">
server {
    listen 80;
    server_name visitor.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
</code-block>

### Deploying to Shared Hosting

1. Upload files to your hosting provider
2. Set up a virtual environment if supported
3. Configure `.htaccess` file for Apache or equivalent for other servers
4. Update the `passenger_wsgi.py` file for specific paths

## ⚙️ Configuration

### Environment Variables

- `SECRET_KEY`: Secret key for Flask sessions
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_HOST`: Redis host
- `REDIS_PORT`: Redis port
- `REDIS_PASSWORD`: Redis password (if needed)
- `REDIS_DB`: Redis database number

### Database Migrations

Create new migrations after model changes:

<code-block language="bash">
flask db migrate -m "Description of changes"
flask db upgrade
</code-block>

## 🌐 Multilingual Support

This application supports English, Korean, and Japanese. To add a new language:

1. Extract messages:

<code-block language="bash">
pybabel extract -F babel.cfg -o messages.pot .
</code-block>

2. Create a new translation:

<code-block language="bash">
pybabel init -i messages.pot -d translations -l [language_code]
</code-block>

3. Edit the `.po` file in `translations/[language_code]/LC_MESSAGES/`

4. Compile translations:

<code-block language="bash">
pybabel compile -d translations
</code-block>

## 🤝 Contributing

Contributions are welcome! Please submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
