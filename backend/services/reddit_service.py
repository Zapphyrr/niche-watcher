import praw
from config import get_settings
from typing import List


class RedditService:
    def __init__(self):
        settings = get_settings()
        self.reddit = praw.Reddit(
            client_id=settings.reddit_client_id,
            client_secret=settings.reddit_client_secret,
            user_agent="niche-watcher/1.0"
        )
    
    def fetch_top_posts(self) -> List[dict]:
        """Récupère top 5 posts du subreddit r/webdev de la semaine"""
        subreddit = self.reddit.subreddit("webdev")
        posts = []
        
        try:
            for submission in subreddit.top("week", limit=5):
                post = {
                    "title": submission.title,
                    "url": submission.url,
                    "content": submission.selftext,
                    "source": "r/webdev",
                    "likes": submission.score,
                    "published_at": submission.created_utc,
                }
                posts.append(post)
        except Exception as e:
            print(f"Error fetching Reddit posts: {e}")
        
        return posts
