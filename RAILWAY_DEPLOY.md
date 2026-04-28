# Déploiement sur Railway

## Configuration rapide

1. **Créer un compte Railway**: https://railway.app

2. **Connecter ton repo GitHub**:
   - New Project → GitHub Repo
   - Sélectionner `niche-watcher`

3. **Créer la base de données PostgreSQL**:
   - Add Service → PostgreSQL
   - Railway va créer une variable `DATABASE_URL`

4. **Configurer les variables d'environnement**:
   - Aller dans le projet Railway
   - Variables → Ajouter les variables de `.env.example`:
     ```
     DATABASE_URL=<auto-generée par Railway>
     EMAIL_BOT_ADDRESS=niche.watcher.bot@gmail.com
     EMAIL_BOT_PASSWORD=<ton app password Gmail>
     JWT_SECRET_KEY=<génère une clé forte: openssl rand -hex 32>
     ENVIRONMENT=production
     FRONTEND_URL=https://your-domain.railway.app
     ```

5. **Déployer**:
   - Railway va détecter le `Procfile`
   - Il va lancer:
     - `web`: API FastAPI (port 8000)
     - `worker`: Scheduler (10 minutes)

## Variables d'environnement importantes

| Variable | Exemple | Notes |
|----------|---------|-------|
| DATABASE_URL | postgresql://user:pw@host:5432/db | Auto-générée par Railway |
| JWT_SECRET_KEY | abc123def456... | CHANGE-MOI! Génère avec: `openssl rand -hex 32` |
| EMAIL_BOT_PASSWORD | Gmail App Password | Pas ton mot de passe Gmail normal |
| ENVIRONMENT | production | Important pour HTTPS |

## Générer un JWT_SECRET_KEY sécurisé

```bash
# Sous Windows (PowerShell)
$bytes = [System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32)
$hex = -join ($bytes | ForEach-Object { $_.ToString("x2") })
echo $hex

# Ou copy-paste cette clé temporaire et change-la immédiatement:
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0
```

## Premier déploiement

1. Push sur GitHub:
   ```bash
   git add .
   git commit -m "Add Railway deployment files"
   git push origin dev_postgre
   ```

2. Railway va automatiquement:
   - Installer les dépendances (`requirements.txt`)
   - Lancer les services (`Procfile`)
   - Créer les tables DB

3. Vérifier le status dans Railway → Deployments

## Post-déploiement

- Tester l'API: `https://your-app.railway.app/api/auth/login`
- Tester la web UI: `https://your-app.railway.app/login`
- Vérifier les logs: Railway → Logs

## Problèmes courants

**"ModuleNotFoundError"**
- Vérifier que `requirements.txt` est à jour: `pip freeze > backend/requirements.txt`

**"database connection refused"**
- Vérifier `DATABASE_URL` dans Railway Variables
- Attendre que PostgreSQL soit fully up

**"Email not sending"**
- Vérifier `EMAIL_BOT_PASSWORD` (app password Gmail, pas le vrai mot de passe)
- Check logs pour les erreurs SMTP

## Architecture Railway

```
Railway Project
├─ web service (FastAPI)
│  └─ Uvicorn on port $PORT (8000)
├─ worker service (Scheduler)
│  └─ Python scheduler.py --loop
└─ PostgreSQL (database)
   └─ niche_watcher
```

## Budget tip

Railway donne 5$ par mois gratuitement. Cette app devrait tenir dedans! ✨
