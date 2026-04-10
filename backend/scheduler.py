"""
Script à exécuter via cron tous les vendredis à 18h
0 18 * * 5 python scheduler.py
"""

from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Post, User
from services import RSSService, RedditService, EmailService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_weekly_digest():
    """Exécute le digest hebdomadaire"""
    
    # Créer les tables si elles n'existent pas
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        logger.info("🚀 Démarrage du scheduler hebdomadaire...")
        
        # Récupérer les posts
        logger.info("📡 Récupération des posts RSS...")
        rss_service = RSSService()
        rss_posts = rss_service.fetch_posts()
        
        logger.info("🔥 Récupération des top posts Reddit...")
        reddit_service = RedditService()
        reddit_posts = reddit_service.fetch_top_posts()
        
        # Combiner tous les posts
        all_posts = rss_posts + reddit_posts
        
        # Déterminer la semaine et l'année ISO
        now = datetime.now()
        week_num = now.isocalendar()[1]
        year_num = now.isocalendar()[0]
        
        # Sauvegarder en base de données
        logger.info(f"💾 Sauvegarde de {len(all_posts)} posts en base de données...")
        for post_data in all_posts:
            post = Post(
                title=post_data.get("title"),
                url=post_data.get("url"),
                content=post_data.get("content"),
                source=post_data.get("source", "unknown"),
                source_name=post_data.get("source_name"),
                likes=post_data.get("likes", 0),
                published_at=post_data.get("published_at"),
                week=week_num,
                year=year_num,
            )
            db.add(post)
        
        db.commit()
        
        # Envoyer les emails
        logger.info("📧 Envoi des emails...")
        email_service = EmailService()
        users = db.query(User).filter(User.subscribed == True).all()
        
        for user in users:
            success = email_service.send_weekly_digest(user.email, all_posts)
            if success:
                logger.info(f"✅ Email envoyé à {user.email}")
                user.last_notification_at = datetime.now()
            else:
                logger.error(f"❌ Erreur d'envoi à {user.email}")
        
        db.commit()
        logger.info("✨ Scheduler hebdomadaire terminé!")
        
    except Exception as e:
        logger.error(f"Erreur dans le scheduler: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    run_weekly_digest()
