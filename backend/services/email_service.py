import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import get_settings
from typing import List
import logging

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.settings = get_settings()
        self.bot_email = self.settings.email_bot_address
        self.bot_password = self.settings.email_bot_password
    
    def send_weekly_digest(self, recipient_email: str, posts: List[dict]) -> bool:
        """Envoie le digest hebdomadaire par email depuis le bot Gmail"""
        try:
            html_content = self._generate_html(posts)
            
            # Créer l'email
            msg = MIMEMultipart()
            msg['From'] = self.bot_email
            msg['To'] = recipient_email
            msg['Subject'] = "📰 Niche Watcher - Résumé de la semaine"
            msg.attach(MIMEText(html_content, 'html'))
            
            # Envoyer via SMTP Gmail depuis le bot
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.bot_email, self.bot_password)
                server.send_message(msg)
            
            logger.info(f"✅ Email sent successfully from {self.bot_email} to {recipient_email}")
            return True
        except Exception as e:
            logger.error(f"❌ Error sending email: {e}")
            return False
    
    def _generate_html(self, posts: List[dict]) -> str:
        """Génère le HTML du digest"""
        html = """
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #f5f5f5; padding: 20px;">
                <div style="background-color: white; padding: 20px; border-radius: 8px;">
                    <h1 style="color: #333;">📰 Niche Watcher - Résumé de la semaine</h1>
                    <p style="color: #666;">Découvre ce qu'il s'est passé cette semaine!</p>
                    <hr style="border: 1px solid #ddd;">
        """
        
        if not posts:
            html += "<p style='color: #999;'>Aucun nouveau post cette semaine.</p>"
        else:
            for post in posts:
                html += f"""
                    <div style="margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #eee;">
                        <h3 style="margin: 0 0 10px 0; color: #333;">
                            <a href="{post.get('url', '#')}" style="color: #0066cc; text-decoration: none;">
                                {post.get('title', 'No title')}
                            </a>
                        </h3>
                        <p style="margin: 5px 0; color: #666; font-size: 12px;">
                            <strong>Source:</strong> {post.get('source', 'Unknown')}
                        </p>
                        <p style="margin: 10px 0; color: #555;">{post.get('content', '')[:200]}...</p>
                    </div>
                """
        
        html += """
                    <hr style="border: 1px solid #ddd; margin-top: 20px;">
                    <p style="color: #999; font-size: 12px; text-align: center;">
                        Niche Watcher - Votre veille simplifiée
                    </p>
                </div>
            </body>
        </html>
        """
        
        return html