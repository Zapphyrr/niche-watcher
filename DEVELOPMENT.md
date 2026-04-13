# 🚀 Niche Watcher - Guide de Développement

## État du Projet (10 Avril 2026)

Ce document résume l'état ACTUEL et les étapes complétées.

### ✅ Complété
- [x] Initialisation Git (commit initial avec 21 files)
- [x] Configuration des sources RSS (HackerNews, Dev.to, CSS-Tricks)
- [x] Migration Email: SMTP → Resend API
- [x] Mise à jour config.py et requirements.txt
- [x] Setup GitHub avec branche `dev`

### ⏳ En Cours
- [ ] Configuration des variables d'environnement (.env)
- [ ] Setup PostgreSQL (Docker)
- [ ] Test local du scheduler
- [ ] Embellissement du template HTML email

### 🔄 À Faire
- [ ] Intégration Reddit API (avec credentials)
- [ ] Déploiement Railway
- [ ] Configuration Cron Job (vendredi 18h)
- [ ] App mobile Flutter

---

## 📚 Architecture

### Backend (Python FastAPI)
```
- main.py: API FastAPI avec endpoints CRUD posts
- scheduler.py: Script exécuté chaque vendredi 18h
- services/
  - rss_service.py: Récupère 5 posts de 3 sources RSS
  - reddit_service.py: Récupère top 5 posts r/webdev/week
  - email_service.py: Envoie digest HTML via Resend API
- models/: Post, User SQLAlchemy
- routes/: API endpoints
- database.py: PostgreSQL connection
- config.py: Pydantic BaseSettings (variables d'env)
```

### Mobile (Flutter)
- App affichage des posts
- À implémenter (brouillon pubspec.yaml seulement)

---

## 🔧 Configuration Requise

### Variables d'Environnement (.env)
Créer `backend/.env` avec:
```env
# Database (PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/niche_watcher

# Email (Resend - https://resend.com)
RESEND_API_KEY=re_xxxxxxxxxxx
SENDER_EMAIL=noreply@niche-watcher.com

# Reddit API (https://reddit.com/prefs/apps)
REDDIT_CLIENT_ID=xxxxxxxxxxxxxxxx
REDDIT_CLIENT_SECRET=xxxxxxxxxxxxxxxx

# API Config
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
```

---

## 🌐 Sources RSS Configurées

1. **HackerNews**: https://news.ycombinator.com/rss
2. **Dev.to**: https://dev.to/feed
3. **CSS-Tricks**: https://css-tricks.com/feed

Chaque source récupère **top 5 posts**.

---

## 📧 Email Service

**Migration complétée**: SMTP → Resend API

```python
# Usage
from services import EmailService
from models import Post

service = EmailService()
posts = [...]  # List[dict]
service.send_weekly_digest("user@example.com", posts)
```

**Template HTML**: Basique, à améliorer (voir `_generate_html()`)

---

## ⏰ Scheduler - Cron Job

**Fréquence**: Chaque vendredi 18h (UTC 0)
```bash
0 18 * * 5 cd /path/to/backend && python scheduler.py
```

**Workflow**:
1. Récupère posts RSS (top 5 × 3 sources)
2. Récupère posts Reddit r/webdev (top 5)
3. Sauvegarde en DB PostgreSQL
4. Envoie email HTML à l'utilisateur

---

## 🚀 Démarrage Local

### Prérequis
- Python 3.9+
- PostgreSQL
- (Optionnel) Docker pour PostgreSQL

### Setup
```bash
cd backend

# Venv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies
pip install -r requirements.txt

# Config
cp .env.example .env
# → Remplir .env avec vos credentials

# Database (via Docker)
docker-compose up -d

# Run API
python main.py

# Test scheduler (manuel)
python scheduler.py
```

---

## 🔐 GitHub Setup

**Branch Protection** (Recommandé sur `main` et `dev`):
- [x] Require pull request reviews (1 minimum)
- [x] Require status checks to pass
- [x] Require branches up to date before merging
- [x] Restrict who can push

---

## 📋 Dépendances Clés

- **fastapi**: Web framework
- **sqlalchemy**: ORM
- **psycopg2**: PostgreSQL driver
- **feedparser**: Parse RSS feeds
- **praw**: Reddit API client
- **resend**: Email service modern
- **python-dotenv**: Gestion .env
- **uvicorn**: ASGI server

Voir `backend/requirements.txt` pour versions exactes.

---

## 🎯 Prochaines Étapes

1. **Créer `.env`** avec credentials (LOCAL SEULEMENT)
2. **Setup PostgreSQL** (docker-compose)
3. **Test local** du scheduler
4. **Embellir template HTML** (design responsive)
5. **Déployer Railway** + configurer Cron
6. **Implémenter mobile** (Flutter)

---

## 📞 Support

Voir `README.md` pour structure du projet.
Pour détails développement: Ce fichier.

---

**Dernière mise à jour**: 10 Avril 2026
**Mainteneur**: [Votre nom]
