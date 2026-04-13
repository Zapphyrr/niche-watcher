"""
Script TEST : pour alimenter la base de données avec des posts de test
"""
from datetime import datetime, timedelta
from database import SessionLocal, engine, Base
from models import Post


def seed_database():
    """Crée des posts de test dans la base de données"""
    
    # S'assurer que les tables existent
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Vérifier si des posts existent déjà
    if db.query(Post).count() > 0:
        print("⚠️  La base de données contient déjà des posts. Aucun ajout effectué.")
        db.close()
        return
    
    # Données de test
    posts_data = [
        {
            "title": "Comment optimiser votre stratégie de contenu sur les réseaux sociaux",
            "url": "https://blog.example.com/social-media-strategy",
            "content": "Découvrez les meilleures pratiques pour optimiser votre présence sur les réseaux sociaux en 2026. Cette analyse approfondie couvre les dernières tendances, les algorithmes et les stratégies éprouvées.",
            "source": "blog",
            "source_name": "Marketing Blog",
            "likes": 234,
            "published_at": datetime.now() - timedelta(days=5),
            "week": 15,
            "year": 2026
        },
        {
            "title": "Les 5 erreurs courantes en SEO que vous devez éviter",
            "url": "https://seo-guide.com/common-mistakes",
            "content": "Une analyse détaillée des erreurs SEO les plus courantes qui pénalisent votre classement. Apprenez comment les corriger facilement et augmenter votre trafic organique.",
            "source": "blog",
            "source_name": "SEO Guide",
            "likes": 567,
            "published_at": datetime.now() - timedelta(days=3),
            "week": 15,
            "year": 2026
        },
        {
            "title": "Python vs JavaScript : Quel langage choisir en 2026?",
            "url": "https://dev-compare.io/python-vs-javascript",
            "content": "Comparaison complète entre Python et JavaScript pour les développeurs. Analyse des forces, faiblesses et cas d'usage de chaque langage.",
            "source": "blog",
            "source_name": "Dev Comparison",
            "likes": 892,
            "published_at": datetime.now() - timedelta(days=2),
            "week": 15,
            "year": 2026
        },
        {
            "title": "Tendances ecommerce 2026 - Ce qui va dominer le marché",
            "url": "https://ecommerce-trends.com/2026-predictions",
            "content": "Les tendances ecommerce qui vont transformer le secteur. Du commerce social au AI shopping, découvrez ce qui attend les commerçants en ligne.",
            "source": "blog",
            "source_name": "Ecommerce Trends",
            "likes": 445,
            "published_at": datetime.now() - timedelta(days=1),
            "week": 15,
            "year": 2026
        },
        {
            "title": "Comment monétiser votre audience en ligne",
            "url": "https://monetization-guide.com/strategies",
            "content": "Guide complet pour monétiser votre audience. Découvrez les meilleures stratégies pour générer des revenus passifs et actifs.",
            "source": "blog",
            "source_name": "Monetization Guide",
            "likes": 678,
            "published_at": datetime.now() - timedelta(hours=12),
            "week": 15,
            "year": 2026
        },
        {
            "title": "L'IA va-t-elle remplacer les développeurs?",
            "url": "https://ai-discussion.reddit.com/posts/12345",
            "content": "Une discussion intéressante sur Reddit concernant l'impact de l'IA sur les métiers de développeur. Les utilisateurs partagent leurs préoccupations et opportunités.",
            "source": "reddit",
            "source_name": "r/programming",
            "likes": 1203,
            "published_at": datetime.now() - timedelta(days=4),
            "week": 15,
            "year": 2026
        },
        {
            "title": "Startup de dropshipping: rentable ou piège?",
            "url": "https://business-reddit.com/posts/67890",
            "content": "Discussion Reddit sur la viabilité du dropshipping en 2026. Des entrepreneurs partagent leurs expériences vraies.",
            "source": "reddit",
            "source_name": "r/entrepreneur",
            "likes": 856,
            "published_at": datetime.now() - timedelta(days=2),
            "week": 15,
            "year": 2026
        },
        {
            "title": "Nouveau framework frontend révolutionnaire",
            "url": "https://dev-news.com/new-framework",
            "content": "Un nouveau framework frontend promet de révolutionner la façon dont nous développons des applications web. Première impressions et benchmark.",
            "source": "blog",
            "source_name": "Dev News",
            "likes": 345,
            "published_at": datetime.now() - timedelta(hours=6),
            "week": 15,
            "year": 2026
        },
        {
            "title": "Cryptomonnaies 2026: La prochaine vague?",
            "url": "https://crypto-analysis.com/2026-forecast",
            "content": "Analyse des tendances crypto pour 2026. Quelles sont les pièces prometteuses? Quel est le meilleur moment pour investir?",
            "source": "blog",
            "source_name": "Crypto Analysis",
            "likes": 512,
            "published_at": datetime.now() - timedelta(days=1),
            "week": 15,
            "year": 2026
        },
        {
            "title": "Marketing d'affiliation: Guide complet pour débutants",
            "url": "https://affiliate-guide.com/beginners",
            "content": "Tout ce que vous devez savoir pour commencer avec le marketing d'affiliation. Stratégies, outils et sources de revenue.",
            "source": "blog",
            "source_name": "Affiliate Guide",
            "likes": 734,
            "published_at": datetime.now() - timedelta(days=3),
            "week": 14,
            "year": 2026
        },
    ]
    
    # Insérer les posts
    for post_data in posts_data:
        post = Post(**post_data)
        db.add(post)
    
    # Commiter les changements
    db.commit()
    print(f"✅ {len(posts_data)} posts ajoutés avec succès!")
    
    # Afficher les posts ajoutés
    posts = db.query(Post).all()
    print(f"\n📊 Total de posts en base de données: {len(posts)}")
    for post in posts:
        print(f"  - {post.title[:60]}... ({post.source})")
    
    db.close()


if __name__ == "__main__":
    seed_database()
