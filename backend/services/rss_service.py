import feedparser
import requests
from typing import List
from models import Besthackernews
from database import SessionLocal, engine, Base
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re
#scrap du content du best post HN
import trafilatura

db = SessionLocal()
class RSSService:
    def __init__(self):
        self.other_feeds = [
            "https://css-tricks.com/category/articles/feed/",
        ]
    
    def _scrape_hn_day(self, date_str: str) -> List[dict]:
        """Scrape les posts HN pour un jour spécifique"""
        posts = []
        url = f"https://news.ycombinator.com/front?day={date_str}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Trouver tous les posts (structure HN: tr avec classe "athing")
            rows = soup.find_all('tr', class_='athing')
            
            print(f"📄 Jour {date_str}: {len(rows)} posts trouvés")
            
            for row in rows[:10]:  # Limiter à 10 posts par jour
                try:
                    # Récupérer le titre et le lien
                    title_cell = row.find('span', class_='titleline')
                    if not title_cell:
                        continue
                    
                    link_elem = title_cell.find('a')
                    if not link_elem:
                        continue
                    
                    title = link_elem.get_text()
                    url_post = link_elem.get('href', '')
                    post_id = row.get('id', '')
                    
                    # Récupérer le score depuis la ligne suivante
                    score_row = row.find_next('tr')
                    score = 0
                    if score_row:
                        score_text = score_row.find('span', class_='score')
                        if score_text:
                            score_match = re.search(r'(\d+)', score_text.get_text())
                            if score_match:
                                score = int(score_match.group(1))
                    
                    post = {
                        "title": title,
                        "url": url_post if url_post.startswith('http') else f"https://news.ycombinator.com/{url_post}",
                        "content": "",
                        "source": "HackerNews",
                        "likes": score,
                        "published_at": datetime.strptime(date_str, "%Y-%m-%d"),
                    }
                    posts.append(post)
                    
                except Exception as e:
                    print(f"  ⚠️  Erreur parsing post: {e}")
                    continue
            
            print(f"  ✅ {len(posts)} posts parsés")
            return posts
        
        except Exception as e:
            print(f"❌ Erreur scraping HN {date_str}: {e}")
            return []
    
    def _fetch_hackernews_posts(self) -> List[dict]:
        """Récupère les posts HN jour par jour (derniers 7 jours)"""
        all_posts = []
        
        print("📡 Scraping HackerNews (7 derniers jours)...")
        
        # Scraper jour par jour (du jour précédent jusqu'à j-7)
        for i in range(1, 8):
            date = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
            day_posts = self._scrape_hn_day(date)
            all_posts.extend(day_posts)
        
        # Trier par score (décroissant) et prendre le top 10
        all_posts.sort(key=lambda x: x["likes"], reverse=True)
        top_posts = all_posts[:10]
        
        print(f"\n🔝 Top 10 posts HN de la semaine:")
        for i, post in enumerate(top_posts, 1):
            print(f"  {i}. {post['title'][:60]}... ({post['likes']} points), sortis le {post['published_at'].strftime('%Y-%m-%d')}")
            #Save du top1 HN dans la BD
            if i == 1:
                print(f"  💾 Sauvegarde du top post HN {post['title']} dans la base de données...")
                best_post = Besthackernews(
                    title=post['title'],
                    url=post['url'],
                    content=post['content'],
                    source=post['source'],
                    likes=post['likes'],
                    published_at=post['published_at']
                )
                if best_post.content == "":
                    #scrap du content du best post HN
                    url = best_post.url
                    downloaded = trafilatura.fetch_url(url)
                    if downloaded:
                        best_post.content = trafilatura.extract(downloaded, include_comments=False)[:500]
                db.add(best_post)
                db.commit()

        return top_posts
    
    def _scrape_devto(self) -> List[dict]:
        """Récupère les top articles de dev.to via API"""
        posts = []
        url = "https://dev.to/api/articles?per_page=5&top=7days"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            articles = response.json()
            
            print(f"📡 Scraping Dev.to (top/week via API)...")
            print(f"📄 {len(articles)} articles trouvés")
            
            for article in articles:
                try:
                    post = {
                        "title": article.get("title", ""),
                        "url": article.get("url", ""),
                        "content": article.get("description", "")[:500],  # Limiter à 500 chars
                        "source": "dev.to",
                        "likes": article.get("positive_reactions_count", 0),
                        "published_at": datetime.fromisoformat(article.get("published_at", "").replace('Z', '+00:00')) if article.get("published_at") else datetime.utcnow(),
                    }
                    posts.append(post)
                    
                except Exception as e:
                    print(f"  ⚠️  Erreur parsing article: {e}")
                    continue
            
            print(f"  ✅ {len(posts)} articles parsés")
            return posts
        
        except Exception as e:
            print(f"❌ Erreur fetching Dev.to API: {e}")
            return []
    
    """
    def _scrape_devto(self) -> List[dict]:
        "scrape le top 5 posts de dev.to"
        posts = []
        url = "https://dev.to/top/week/"
        
        try:
            feed = feedparser.parse(url)
            print(f"📡 Récupération de {feed.feed.title}...")
            
            for entry in feed.entries[:5]:  # Top 5 posts
                post = {
                    "title": entry.title,
                    "url": entry.link,
                    "content": entry.get("summary", ""),
                    "source": feed.feed.title,
                    "likes": 0,
                    "published_at": datetime(*entry.published_parsed[:6]) if entry.get("published_parsed") else datetime.utcnow(),
                }
                posts.append(post)
            
            print(f"✅ {len(posts)} posts de {feed.feed.title}")
            return posts
        
        except Exception as e:
            print(f"❌ Erreur fetching Dev.to: {e}")
            return []
    """
    
    def _fetch_other_feeds(self) -> List[dict]:
        """Récupère les posts des autres sources RSS"""
        
        posts = []
        
        for feed_url in self.other_feeds:
            try:
                feed = feedparser.parse(feed_url)
                print(f"📡 Récupération de {feed.feed.title}...")
                
                for entry in feed.entries[:5]:  # Top 5 posts par source
                    post = {
                        "title": entry.title,
                        "url": entry.link,
                        "content": entry.get("summary", ""),
                        "source": feed.feed.title,
                        "likes": 0,
                        "published_at": datetime(*entry.published_parsed[:6]) if entry.get("published_parsed") else datetime.utcnow(),
                    }
                    posts.append(post)
                
                print(f"✅ {len(feed.entries[:5])} posts de {feed.feed.title}")
            except Exception as e:
                print(f"❌ Erreur fetching {feed_url}: {e}")
        
        return posts
    
    def fetch_posts(self) -> List[dict]:
        """Récupère tous les posts (HN top 10 + Dev.to + autres sources)"""
        hn_posts = self._fetch_hackernews_posts()
        devto_posts = self._scrape_devto()
        other_posts = self._fetch_other_feeds()
        
        print(f"\n🎉 Total: {len(hn_posts)} posts HN + {len(devto_posts)} posts Dev.to + {len(other_posts)} posts autres sources")
        return hn_posts + devto_posts + other_posts
