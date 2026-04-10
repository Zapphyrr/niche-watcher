import feedparser
from typing import List
from datetime import datetime


class RSSService:
    def __init__(self):
        # Configure vos 3 blogs dev ici
        self.feeds = [
            "https://example-blog1.com/feed.xml",
            "https://example-blog2.com/feed.xml",
            "https://example-blog3.com/feed.xml",
        ]
    
    def fetch_posts(self) -> List[dict]:
        """Récupère les posts RSS de tous les blogs"""
        posts = []
        
        for feed_url in self.feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]:  # Top 5 posts
                    post = {
                        "title": entry.title,
                        "url": entry.link,
                        "content": entry.get("summary", ""),
                        "source": feed.feed.title,
                        "published_at": datetime(*entry.published_parsed[:6]),
                    }
                    posts.append(post)
            except Exception as e:
                print(f"Error fetching RSS from {feed_url}: {e}")
        
        return posts
