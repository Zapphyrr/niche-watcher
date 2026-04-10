from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Post

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("/")
def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Récupère les posts par page"""
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts


@router.get("/latest")
def get_latest_posts(limit: int = 10, db: Session = Depends(get_db)):
    """Récupère les posts les plus récents"""
    posts = db.query(Post).order_by(Post.created_at.desc()).limit(limit).all()
    return posts


@router.get("/week/{week}")
def get_posts_by_week(week: int, year: int = 2026, db: Session = Depends(get_db)):
    """Récupère les posts d'une semaine donnée"""
    posts = db.query(Post).filter(
        Post.week == week,
        Post.year == year
    ).all()
    return posts
