from .posts import router as posts_router
from .auth import router as auth_router

__all__ = ["posts_router", "auth_router"]
