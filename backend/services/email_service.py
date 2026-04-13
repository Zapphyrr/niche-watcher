from resend import Resend
from config import get_settings
from typing import List
import logging

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.settings = get_settings()
        self.client = Resend(api_key=self.settings.resend_api_key)
    
    def send_weekly_digest(self, recipient_email: str, posts: List[dict]) -> bool:
        """Envoie le digest hebdomadaire par email avec Resend"""
        try:
            # Créer le contenu HTML
            html_content = self._generate_html(posts)
            
            # Envoyer l'email via Resend
            response = self.client.emails.send({
                "from": self.settings.sender_email,
                "to": recipient_email,
                "subject": "Niche Watcher - Résumé de la semaine",
                "html": html_content
            })
            
            logger.info(f"Email sent successfully to {recipient_email}")
            return True
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def _generate_html(self, posts: List[dict]) -> str:
        """Génère le HTML du digest premium"""
        
        # Créer les cards pour chaque post
        posts_html = ""
        for i, post in enumerate(posts, 1):
            source = post.get('source', 'Unknown')
            # Couleur différente par source
            colors = {
                "Hacker News": "#FF6600",
                "Dev.to": "#000000",
                "CSS-Tricks": "#0066CC",
                "r/webdev": "#FF4500"
            }
            color = colors.get(source, "#0066CC")
            
            posts_html += f"""
            <div style="margin-bottom: 24px; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden; background: #ffffff;">
                <div style="background: {color}; padding: 12px 20px; color: white;">
                    <span style="font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">#{i} • {source}</span>
                </div>
                <div style="padding: 20px;">
                    <h3 style="margin: 0 0 12px 0; font-size: 18px; font-weight: 600; color: #111827; line-height: 1.4;">
                        <a href="{post.get('url', '#')}" style="color: #111827; text-decoration: none;">{post.get('title', 'Sans titre')}</a>
                    </h3>
                    <p style="margin: 0; font-size: 14px; color: #6b7280; line-height: 1.6;">
                        {post.get('content', 'Pas de description')[:200]}...
                    </p>
                    <div style="margin-top: 16px;">
                        <a href="{post.get('url', '#')}" style="display: inline-block; padding: 10px 20px; background: {color}; color: white; text-decoration: none; border-radius: 6px; font-size: 14px; font-weight: 600;">
                            Lire l'article →
                        </a>
                    </div>
                </div>
            </div>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Niche Watcher - Résumé Hebdo</title>
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background: #f9fafb; margin: 0; padding: 0; color: #374151;">
            
            <!-- Container Principal -->
            <div style="max-width: 600px; margin: 0 auto; background: #ffffff;">
                
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center; color: white;">
                    <div style="font-size: 48px; margin-bottom: 12px;"></div>
                    <h1 style="margin: 0 0 8px 0; font-size: 32px; font-weight: 700;">Niche Watcher</h1>
                    <p style="margin: 0; font-size: 16px; opacity: 0.95;">Votre résumé de l'actualité devlopeur</p>
                </div>
                
                <!-- Hero Text -->
                <div style="padding: 32px 20px; text-align: center; background: #f3f4f6;">
                    <p style="margin: 0; font-size: 16px; color: #374151; line-height: 1.6;">
                        <strong>Samedi matin, avec votre café</strong><br>
                        Découvrez les meilleures actus dev de la semaine, filtrées et organisées pour vous.
                    </p>
                </div>
                
                <!-- Contenu Principal -->
                <div style="padding: 32px 20px;">
                    <h2 style="margin: 0 0 24px 0; font-size: 22px; font-weight: 600; color: #111827;">Cette semaine en vedette 🔥</h2>
                    
                    {posts_html}
                    
                </div>
                
                <!-- Stats Footer -->
                <div style="background: #f3f4f6; padding: 24px 20px; text-align: center; border-top: 1px solid #e5e7eb;">
                    <p style="margin: 0; font-size: 13px; color: #6b7280;">
                        <strong>{len(posts)} articles</strong> sélectionnés de <strong>HackerNews</strong>, <strong>Dev.to</strong> et <strong>CSS-Tricks</strong>
                    </p>
                </div>
                
                <!-- CTA Button -->
                <div style="padding: 32px 20px; text-align: center;">
                    <a href="https://niche-watcher.com/app" style="display: inline-block; padding: 14px 32px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 16px; transition: transform 0.2s;">
                        Ouvre l'app mobile
                    </a>
                </div>
                
                <!-- Footer -->
                <div style="background: #1f2937; color: white; padding: 24px 20px; text-align: center; font-size: 13px; border-top: 1px solid #374151;">
                    <p style="margin: 0 0 12px 0;">
                        © 2026 Niche Watcher • <a href="https://niche-watcher.com" style="color: #a78bfa; text-decoration: none;">niche-watcher.com</a>
                    </p>
                    <p style="margin: 0; opacity: 0.7;">
                        Envoyé chaque vendredi soir ⏰ | <a href="#" style="color: #a78bfa; text-decoration: none;">Gérer tes préférences</a>
                    </p>
                </div>
                
            </div>
            
        </body>
        </html>
        """
        
        return html
