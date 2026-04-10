import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import get_settings
from typing import List


class EmailService:
    def __init__(self):
        self.settings = get_settings()
    
    def send_weekly_digest(self, recipient_email: str, posts: List[dict]) -> bool:
        """Envoie le digest hebdomadaire par email"""
        try:
            # Créer le contenu HTML
            html_content = self._generate_html(posts)
            
            # Créer le message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "📰 Niche Watcher - Résumé de la semaine"
            msg["From"] = self.settings.smtp_username
            msg["To"] = recipient_email
            
            html_part = MIMEText(html_content, "html")
            msg.attach(html_part)
            
            # Envoyer l'email
            with smtplib.SMTP(self.settings.smtp_server, self.settings.smtp_port) as server:
                server.starttls()
                server.login(self.settings.smtp_username, self.settings.smtp_password)
                server.sendmail(
                    self.settings.smtp_username,
                    recipient_email,
                    msg.as_string()
                )
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
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
