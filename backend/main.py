from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from database import Base, engine, get_db
from routes import posts_router, auth_router
from models import Post, User
from services import decode_access_token
from pathlib import Path
import asyncio
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - créer les tables avec timeout
    try:
        # Timeout de 10 secondes pour l'initialisation
        await asyncio.wait_for(
            asyncio.to_thread(lambda: Base.metadata.create_all(bind=engine)),
            timeout=10.0
        )
        logger.info("✅ Database tables initialized")
    except asyncio.TimeoutError:
        logger.warning("⚠️ Database initialization timed out, continuing anyway")
    except Exception as e:
        logger.warning(f"⚠️ Database initialization failed: {e}, continuing anyway")
    
    yield
    # Shutdown

app = FastAPI(title="Niche Watcher API", lifespan=lifespan) 

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
app.include_router(auth_router)


def _get_authenticated_user(request: Request, db):
    token = request.cookies.get("access_token")
    if not token:
        return None

    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub", "0"))
    except (ValueError, TypeError):
        return None

    return db.query(User).filter(User.id == user_id).first()


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/logout")
def logout_page():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("access_token")
    return response


@app.get("/")
def read_root(request: Request):
    """Page d'accueil"""
    db = next(get_db())
    try:
        user = _get_authenticated_user(request, db)
        if user is None:
            return RedirectResponse(url="/login", status_code=303)

        total_posts = db.query(Post).count()
        stats = {
            "total_posts": total_posts,
            "sources": 3,  # RSS, Reddit, Email
            "users_tracking": db.query(User).count()
        }
        return templates.TemplateResponse("index.html", {"request": request, "stats": stats, "user": user})
    finally:
        db.close()


@app.get("/posts")
def get_posts_page(request: Request, page: int = 1, sort: str = "latest", week: int = None):
    """Page des posts avec pagination"""
    db = next(get_db())
    try:
        user = _get_authenticated_user(request, db)
        if user is None:
            return RedirectResponse(url="/login", status_code=303)

        limit = 10
        skip = (page - 1) * limit
        
        # Récupérer les top 1 posts par source (pour "à la une")
        featured_posts = {}
        featured_ids = []
        sources = db.query(Post.source).distinct().all()
        for source_tuple in sources:
            source = source_tuple[0]
            top_post = db.query(Post).filter(Post.source == source).order_by(Post.likes.desc(), Post.created_at.desc()).first()
            if top_post:
                featured_posts[source] = top_post
                featured_ids.append(top_post.id)
        
        query = db.query(Post)
        
        # Exclure les posts déjà en "à la une"
        if featured_ids:
            query = query.filter(~Post.id.in_(featured_ids))
        
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
                "featured_posts": featured_posts,
                "page": page,
                "has_next": has_next,
                "total_posts": total_posts,
                "user": user,
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
