from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from database import Base, engine, get_db
from routes import posts_router
from models import Post
from sqlalchemy.orm import Session
from pathlib import Path

settings = get_settings()

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Niche Watcher API")

# Configuration des templates
templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url] if settings.environment == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes API
app.include_router(posts_router)


@app.get("/")
def read_root(request: Request):
    """Page d'accueil"""
    db = next(get_db())
    try:
        total_posts = db.query(Post).count()
        stats = {
            "total_posts": total_posts,
            "sources": 3,  # RSS, Reddit, Email
            "users_tracking": 1
        }
        return templates.TemplateResponse("index.html", {"request": request, "stats": stats})
    finally:
        db.close()


@app.get("/posts")
def get_posts_page(request: Request, page: int = 1, sort: str = "latest", week: int = None):
    """Page des posts avec pagination"""
    db = next(get_db())
    try:
        limit = 10
        skip = (page - 1) * limit
        
        query = db.query(Post)
        
        if week:
            query = query.filter(Post.week == week)
        
        if sort == "latest":
            query = query.order_by(Post.created_at.desc())
        else:
            query = query.order_by(Post.created_at.asc())
        
        total_posts = query.count()
        posts = query.offset(skip).limit(limit).all()
        
        has_next = total_posts > (page * limit)
        
        return templates.TemplateResponse(
            "posts.html",
            {
                "request": request,
                "posts": posts,
                "page": page,
                "has_next": has_next,
                "total_posts": total_posts
            }
        )
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
    )
