# 🚀 Guide de Développement - Niche Watcher

Ce guide vous permet de configurer et lancer le projet Niche Watcher sur votre machine.

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir:
- **Python 3.8+** instalé
- **PostgreSQL 14+** installé et en cours d'exécution
- **Git** (optionnel, pour cloner le repo)

### Vérifier l'installation

```bash
python --version
psql --version
```

---

## 1️⃣ Cloner le projet

```bash
git clone https://github.com/Zapphyrr/niche-watcher.git
cd niche-watcher/backend
```

---

## 2️⃣ Configurer PostgreSQL

### Étape 1: Accéder à PostgreSQL

```bash
psql -U postgres
```

### Étape 2: Créer la base de données et l'utilisateur

```sql
CREATE USER niche_watcher WITH PASSWORD 'your_secure_password';
CREATE DATABASE niche_watcher OWNER niche_watcher;
ALTER ROLE niche_watcher SET client_encoding TO 'utf8';
ALTER ROLE niche_watcher SET default_transaction_isolation TO 'read committed';
ALTER ROLE niche_watcher SET default_transaction_deferrable TO on;
ALTER ROLE niche_watcher SET timezone TO 'UTC';
\q
```

⚠️ **Remplacez `your_secure_password` par un mot de passe sécurisé!**

---

## 3️⃣ Créer l'environnement virtuel

```bash
# Créer le venv
python -m venv venv

# Activer le venv
# Sur Windows:
venv\Scripts\activate
# Sur macOS/Linux:
source venv/bin/activate
```

Vous devriez voir `(venv)` au début de votre prompt.

---

## 4️⃣ Configurer les variables d'environnement

### Créer le fichier `.env`

Créez un fichier `.env` dans le répertoire `backend`:

```
# Database
DATABASE_URL=postgresql://niche_watcher:your_secure_password@localhost:5432/niche_watcher

# Email (Resend)
RESEND_API_KEY=your_resend_api_key
SENDER_EMAIL=noreply@niche-watcher.com

# API
API_HOST=0.0.0.0
API_PORT=8000

# Reddit (optionnel pour le moment)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret

# Frontend URL for CORS
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
```

⚠️ **Remplacez les valeurs par vos clés réelles!**

---

## 5️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 6️⃣ Créer les tables dans PostgreSQL

```bash
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine); print('✅ Tables créées!')"
```

---

## 7️⃣ Alimenter la base de données (optionnel)

Pour ajouter des posts de test:

```bash
python seed.py
```

Cela ajoute 10 posts d'exemple à la base de données.

---

## 8️⃣ Lancer le serveur

### Mode développement (avec rechargement automatique)

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Mode production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 🌐 Accéder à l'application

Une fois le serveur lancé:

- **Interface web**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **API Documentation (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 📝 Structure du projet

```
niche-watcher/
├── backend/
│   ├── main.py              # Point d'entrée FastAPI
│   ├── config.py            # Configuration (variables d'env)
│   ├── database.py          # Connexion PostgreSQL
│   ├── seed.py              # Script pour alimenter la DB
│   ├── requirements.txt      # Dépendances Python
│   ├── models/
│   │   ├── __init__.py
│   │   ├── post.py          # Modèle Post
│   │   └── user.py          # Modèle User
│   ├── routes/
│   │   ├── __init__.py
│   │   └── posts.py         # Routes API pour les posts
│   ├── services/
│   │   ├── __init__.py
│   │   ├── email_service.py # Service email (Resend)
│   │   ├── reddit_service.py # Service Reddit
│   │   └── rss_service.py   # Service RSS
│   └── templates/           # Templates HTML
│       ├── base.html       # Template de base
│       ├── index.html      # Page d'accueil
│       └── posts.html      # Page des posts
├── mobile/                  # Application Flutter
│   └── ...
└── docker-compose.yml       # Configuration Docker
```

---

## 📚 Endpoints API disponibles

### Posts

```
GET /api/posts/                     # Récupérer tous les posts (pagination)
GET /api/posts/latest               # Récupérer les derniers posts
GET /api/posts/week/{week}?year=... # Récupérer les posts d'une semaine
```

### Pages HTML

```
GET /                       # Page d'accueil
GET /posts                  # Liste des posts avec pagination
```

---

## 🔧 Commandes utiles

### Vérifier la connexion à PostgreSQL

```bash
psql -U niche_watcher -d niche_watcher -c "SELECT COUNT(*) FROM posts;"
```

### Afficher tous les posts

```bash
psql -U niche_watcher -d niche_watcher -c "SELECT title, source FROM posts;"
```

### Ajouter un post manuellement

```sql
INSERT INTO posts (title, url, content, source, source_name, likes, published_at, week, year)
VALUES (
  'Titre du post',
  'https://example.com',
  'Contenu du post',
  'blog',
  'Source',
  0,
  NOW(),
  15,
  2026
);
```

---

## ⚠️ Dépannage

### Erreur: `connection to server at "localhost" failed`
- Vérifiez que PostgreSQL est actif: `psql -U postgres`
- Redémarrez le service PostgreSQL

### Erreur: `ValidationError: Field required [type=missing]`
- Vérifiez que le fichier `.env` est complètement rempli
- Vérifiez la syntaxe de `DATABASE_URL`

### Erreur: `ModuleNotFoundError`
- Assurez-vous que le venv est activé: `(venv)` dans le prompt
- Réinstallez les dépendances: `pip install -r requirements.txt`

---

## 🚀 Prochaines étapes

1. **Configurer l'API Reddit** (voir `.env`)
2. **Configurer Resend Email** (voir `.env`)
3. **Développer les services** (Reddit scraper, RSS parser)
4. **Créer la mobile app** (Flutter)
5. **Déployer en production** (Docker, Cloud)

---

## 📞 Support

Pour toute question, consultez:
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation SQLAlchemy](https://docs.sqlalchemy.org/)
- [Documentation PostgreSQL](https://www.postgresql.org/docs/)

---

**Happy coding! 🎉**
