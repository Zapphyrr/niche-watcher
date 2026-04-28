import feedparser
import requests
from typing import List
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re


class RSSService:
    def __init__(self):
        self.other_feeds = [
            "https://dev.to/feed",
            "https://css-tricks.com/feed",
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
        
        return top_posts
    
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
        """Récupère tous les posts (HN top 10 + autres sources)"""
        hn_posts = self._fetch_hackernews_posts()
        other_posts = self._fetch_other_feeds()
        
        print(f"\n🎉 Total: {len(hn_posts)} posts HN + {len(other_posts)} posts autres sources")
        return hn_posts + other_posts
