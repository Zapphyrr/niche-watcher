# Niche Watcher 👀

Un aggrégateur de contenu dev qui compile les posts RSS des 3 blogs dev + top 5 posts r/webdev en une notification hebdomadaire.

## Stack Tech

- **Backend**: Python FastAPI
- **Mobile**: Flutter
- **Database**: PostgreSQL
- **Scheduler**: Cron (vendredi 18h)
- **Email**: Python (smtplib/SendGrid)
- **Hosting**: Railway

## Structure du projet

```
niche-watcher/
├── backend/          # API FastAPI + Scheduler
│   ├── models/       # Modèles de données
│   ├── services/     # RSS, Reddit, Email
│   ├── routes/       # Endpoints API
│   ├── main.py
│   ├── scheduler.py
│   ├── requirements.txt
│   └── .env.example
├── mobile/           # App Flutter
└── docker-compose.yml
```

## Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

### Mobile

```bash
cd mobile
flutter pub get
flutter run
```

### Database

```bash
docker-compose up -d
```

## Cron Schedule

```bash
0 18 * * 5 cd /path/to/backend && python scheduler.py
```

Tous les vendredis à 18h (6 PM)

## Variables d'environnement

Voir `.env.example` dans le dossier backend.
