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
                "subject": "📰 Niche Watcher - Résumé de la semaine",
                "html": html_content
            })
            
            logger.info(f"Email sent successfully to {recipient_email}")
            return True
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def _generate_html(self, posts: List[dict]) -> str:
        """Génère le HTML du digest"""
        html = """
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h1>📰 Niche Watcher - Résumé de la semaine</h1>
                <p>Découvre ce qu'il s'est passé cette semaine dans l'univers dev!</p>
                <hr>
        """
        
        for post in posts:
            html += f"""
                <div style="margin-bottom: 20px; border-bottom: 1px solid #ddd; padding-bottom: 10px;">
                    <h3><a href="{post.get('url', '#')}">{post.get('title', 'No title')}</a></h3>
                    <p><small>Source: {post.get('source', 'Unknown')}</small></p>
                    <p>{post.get('content', '')[:200]}...</p>
                </div>
            """
        
        html += """
                <hr>
                <p><a href="https://niche-watcher.com/app">Ouvre l'app mobile pour plus de détails »</a></p>
            </body>
        </html>
        """
        
        return html
