import os
import string
import random
import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .database import SessionLocal, engine, Base
from .models import URL
from .crud import create_short_url, get_long_url
from .schemas import URLCreate, URLResponse

Base.metadata.create_all(bind=engine)

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    print("🚀 Connecting to Redis...")
    app.state.redis = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    try:
        pong = await app.state.redis.ping()
        print(f"✅ Redis connected: {pong}")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")

    yield  # Application runs here
    
    print("🔴 Closing Redis connection...")
    await app.state.redis.aclose()


# Initialize FastAPI with lifespan
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Change this for production)
    allow_credentials=True,
    allow_methods=["*", "GET", "POST", "OPTIONS"],  # Allow all HTTP methods
    allow_headers=["*", "Content-Type", "Authorization", "ngrok-skip-browser-warning"],  # Allow all headers
)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Generate random short URL
def generate_short_url(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.post("/shorten", response_model=URLResponse)
async def shorten_url(url: URLCreate, db: Session = Depends(get_db)):
    """Shorten a URL and store it in the database + Redis cache."""
    short_url = generate_short_url()
    
    # Store in PostgreSQL
    stored_url = create_short_url(db, short_url, url.long_url)
    
    # Cache in Redis (handle Redis failures gracefully)
    try:
        await app.state.redis.set(short_url, url.long_url)
    except Exception as e:
        print(f"⚠️ Redis cache error: {e}")

    return {"short_url": short_url, "long_url": stored_url.long_url}

@app.get("/health", status_code=200)
def health():
    return {"status": "ok"}

@app.get("/{short_url}")
async def redirect_url(short_url: str, db: Session = Depends(get_db)):
    """Redirect to the original URL from Redis (cache) or PostgreSQL (fallback)."""

    # Try Redis first
    try:
        cached_url = await app.state.redis.get(short_url)
        if cached_url:
            print("🔗 Redirecting (from Redis):", cached_url)
            return RedirectResponse(url=cached_url, status_code=302)
    except Exception as e:
        print(f"⚠️ Redis cache retrieval error: {e}")

    # If not found in Redis, try PostgreSQL
    url_entry = get_long_url(db, short_url)
    if url_entry is None:
        raise HTTPException(status_code=404, detail="URL not found")

    # Cache in Redis
    try:
        await app.state.redis.set(short_url, url_entry.long_url)
    except Exception as e:
        print(f"⚠️ Redis cache update error: {e}")

    print("🔗 Redirecting (from DB):", url_entry.long_url)
    return RedirectResponse(url=url_entry.long_url, status_code=302)
