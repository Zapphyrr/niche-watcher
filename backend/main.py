from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from database import Base, engine
from routes import posts_router

settings = get_settings()

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Niche Watcher API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url] if settings.environment == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(posts_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Niche Watcher API"}


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
