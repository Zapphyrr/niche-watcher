from services import RSSService
from datetime import datetime

rss = RSSService()
posts = rss.fetch_posts()

print(f"Récupéré {len(posts)} posts RSS:")
for post in posts:
    print(f" - {post['title']} ({post['source']}) - Publié le {post['published_at'].strftime('%Y-%m-%d %H:%M:%S')}")    
    print(f"   URL: {post['url']}")
    print(f"   Source: {post['source']}")