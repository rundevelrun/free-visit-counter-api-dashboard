# Visitor Counter

A lightweight, easy-to-use visitor counter for websites with a beautiful dashboard and API.

![Visitor Counter Dashboard](https://via.placeholder.com/800x400?text=Visitor+Counter+Dashboard)

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Installation](#installation)
- [Deployment](#deployment)
- [Configuration](#configuration)
- [Internationalization](#internationalization)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Real-time Tracking**: Track visitors in real-time with accurate counting and duplicate prevention
- **Responsive Dashboard**: View your visitor statistics on any device with our responsive dashboard
- **Easy Integration**: Simple API makes it easy to integrate with any website or application
- **Multiple Websites**: Track visitors across multiple domains with a single account
- **Multilingual Support**: Available in English, Korean, and Japanese
- **Dark/Light Theme**: Switch between dark and light themes for comfortable viewing
- **Duplicate Prevention**: Uses Redis with a 20-minute TTL to prevent counting the same visitor multiple times
- **Timezone Support**: Calculates "today" based on the visitor's timezone

## 🚀 Quick Start

### 1. Add this script to your website

```html
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
```

### 2. View your dashboard

Go to `https://visitor.6developer.com/login` and enter your domain to view your visitor statistics.

## 📊 API Documentation

### Base URL

```
https://visitor.6developer.com
```

### Record a Visit

```
POST /visit
```

**Request Body:**

```json
{
  "domain": "example.com",
  "timezone": "America/New_York" // Optional, defaults to UTC
}
```

**Response:**

```json
{
  "domain": "example.com",
  "totalCount": 42,
  "todayCount": 5
}
```

### Get Visit Statistics

```
GET /visit?domain=example.com
```

**Response:**

```json
{
  "domain": "example.com",
  "totalCount": 42,
  "todayCount": 5,
  "todayDate": "2023-04-15",
  "createdAt": "2023-01-01T00:00:00"
}
```

For more details, see the [API Documentation](https://visitor.6developer.com/api-docs).

## 🛠️ Installation

### Prerequisites

- Python 3.9+
- PostgreSQL
- Redis

### Setup

1. Clone the repository

```bash
git clone https://github.com/yourusername/visitor-counter.git
cd visitor-counter
```

2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set up environment variables

Create a `.env` file in the project root:

```
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://username:password@localhost/visitor_counter
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
```

5. Initialize the database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Run the application

```bash
flask run
```

## 🚀 Deployment

### Deploying to a VPS

1. Set up a Python environment on your server
2. Install PostgreSQL and Redis
3. Clone the repository and follow the installation steps
4. Set up a production WSGI server (Gunicorn, uWSGI)
5. Configure Nginx as a reverse proxy

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name visitor.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Deploying to Shared Hosting

1. Upload the files to your hosting provider
2. Set up a virtual environment if supported
3. Configure the `.htaccess` file for Apache or equivalent for other servers
4. Update the `passenger_wsgi.py` file with your specific paths

## ⚙️ Configuration

### Environment Variables

- `SECRET_KEY`: Secret key for Flask sessions
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_HOST`: Redis host
- `REDIS_PORT`: Redis port
- `REDIS_PASSWORD`: Redis password (if required)
- `REDIS_DB`: Redis database number

### Database Migrations

To create a new migration after changing models:

```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

## 🌐 Internationalization

The application supports English, Korean, and Japanese. To add a new language:

1. Extract messages:

```bash
pybabel extract -F babel.cfg -o messages.pot .
```

2. Create a new translation:

```bash
pybabel init -i messages.pot -d translations -l [language_code]
```

3. Edit the `.po` file in `translations/[language_code]/LC_MESSAGES/`

4. Compile translations:

```bash
pybabel compile -d translations
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
