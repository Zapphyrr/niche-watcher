# Niche Watcher - Development Guide

This file is the handoff note for the next developer. It reflects the current state of the app, what is already working, and what should come next.

## Current Goal

Niche Watcher aggregates content into a shared database and sends a weekly digest. The scheduler is intentionally shared for everyone; client apps should read from the database, not run their own scraping jobs. The next major feature is authentication so users can sign up, log in, and be tied to subscriptions before deployment.

## What Is Already Working

- FastAPI backend with template routes on `localhost:8000`.
- PostgreSQL schema and SQLAlchemy models.
- Hacker News ingestion through HTML scraping, not RSS.
- Dev.to and CSS-Tricks ingestion through RSS.
- Gmail SMTP email delivery.
- Scheduler execution with a test loop mode.
- Jinja2 frontend pages with a dark theme.
- PowerShell profile customization with timestamps in the prompt.

## Setup

### Prerequisites

- Python 3.8+.
- PostgreSQL 14+ running locally.
- Git, if you want to clone the repository.

Check the local tools:

```bash
python --version
psql --version
```

### Clone the project

```bash
git clone https://github.com/Zapphyrr/niche-watcher.git
cd niche-watcher/backend
```

### Create the database

```bash
psql -U postgres
```

```sql
CREATE USER niche_watcher WITH PASSWORD 'your_secure_password';
CREATE DATABASE niche_watcher OWNER niche_watcher;
ALTER ROLE niche_watcher SET client_encoding TO 'utf8';
ALTER ROLE niche_watcher SET default_transaction_isolation TO 'read committed';
ALTER ROLE niche_watcher SET default_transaction_deferrable TO on;
ALTER ROLE niche_watcher SET timezone TO 'UTC';
\q
```

### Create the virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### Configure environment variables

Create `backend/.env`:

```env
DATABASE_URL=postgresql://niche_watcher:your_secure_password@localhost:5432/niche_watcher
EMAIL_BOT_ADDRESS=your_gmail@gmail.com
EMAIL_BOT_PASSWORD=your_app_specific_password
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create tables and seed data

```bash
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine); print('Tables created')"
python seed.py
```

## Run The App

### API and web UI

Development:

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Production style:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Open:

- http://localhost:8000
- http://localhost:8000/posts
- http://localhost:8000/docs
- http://localhost:8000/redoc
- http://localhost:8000/health

### Scheduler

The scheduler currently runs as a shared job for the whole app. In production it should run once on a schedule; for local testing it can loop every 10 minutes.

```bash
python scheduler.py
python scheduler.py --loop
```

`--loop` is the test mode. It repeatedly runs the digest job every 10 minutes.

## Current Data Flow

1. The scheduler calls `RSSService.fetch_posts()`.
2. Hacker News is scraped from `https://news.ycombinator.com/front?day=YYYY-MM-DD` for the last 7 days.
3. Up to 10 posts are collected per day, then all posts are sorted by score and the top 10 are kept.
4. Dev.to and CSS-Tricks are fetched from RSS, with the top 5 entries taken from each feed.
5. The scheduler saves the combined post list to PostgreSQL with ISO week and year metadata.
6. The email service sends the digest through Gmail SMTP.

### Hacker News implementation details

- HTML parsing uses BeautifulSoup.
- The score is extracted from the HN score span.
- Posts without a score default to 0.
- This approach replaced RSS/API attempts because the score-aware feed was not reliable enough for the ranking goal.

### Email implementation details

- Provider: Gmail SMTP bot account.
- Sender: `niche.watcher.bot@gmail.com`.
- The email body is HTML formatted.

## Project Structure

```text
niche-watcher/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── scheduler.py
│   ├── seed.py
│   ├── requirements.txt
│   ├── models/
│   │   ├── __init__.py
│   │   ├── post.py
│   │   └── user.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── posts.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── email_service.py
│   │   ├── reddit_service.py
│   │   └── rss_service.py
│   └── templates/
│       ├── base.html
│       ├── index.html
│       └── posts.html
├── mobile/
│   └── lib/
│       ├── main.dart
│       └── screens/
│           └── home_screen.dart
└── docker-compose.yml
```

## Current Routes

### HTML pages

```text
GET /
GET /posts
GET /health
```

### API routes

The posts router is mounted from `routes/posts.py`. The exact endpoints are defined there.

## UI Notes

- The frontend uses Jinja2 templates.
- The design is a dark theme with a purple primary color.
- RSS content is cleaned in the template with `striptags` and truncated for readability.
- The posts page has improved spacing, filtered views, and a styled week selector.

## PowerShell Prompt

The local PowerShell profile was customized so every terminal prompt shows time, user, computer, and path.

```powershell
function prompt {
  $time = "$(Get-Date -Format 'HH:mm:ss')"
  $user = "${env:USERNAME}"
  $computer = "${env:COMPUTERNAME}"
  $path = "$(Get-Location)"

  Write-Host "[$time] " -ForegroundColor Cyan -NoNewline
  Write-Host "$user@$computer" -ForegroundColor Green -NoNewline
  Write-Host ":" -ForegroundColor White -NoNewline
  Write-Host "$path" -ForegroundColor Yellow -NoNewline
  Write-Host "> " -ForegroundColor Magenta -NoNewline

  return " "
}
```

## Authentication Next

This is the next feature to implement.

Recommended direction:

1. Add signup and login endpoints.
2. Hash passwords before storing them.
3. Issue JWT tokens for session handling.
4. Tie users to the existing `users` table.
5. Keep the scheduler shared, but make email delivery user-aware through subscriptions.

Important note: the `User` model already exists with `email`, `device_token`, `subscribed`, `created_at`, and `last_notification_at`. Authentication has not been wired in yet.

## Troubleshooting

- If PostgreSQL is unavailable, verify the service is running and the `DATABASE_URL` is correct.
- If settings validation fails, check the `.env` file for missing values.
- If Python cannot import a package, confirm the virtual environment is activated and reinstall dependencies.

## Useful Checks

```bash
psql -U niche_watcher -d niche_watcher -c "SELECT COUNT(*) FROM posts;"
psql -U niche_watcher -d niche_watcher -c "SELECT title, source FROM posts LIMIT 10;"
```

## Notes For The Next Agent

- Do not split the scheduler by client. It is intentionally shared.
- The client apps should read from the database.
- Authentication is the blocking piece before deployment and sharing the app with other people.
- Once auth is in place, the next logical step is to make the scheduler send digests only to subscribed users.

