from sqlalchemy.orm import Session
from .models import URL

def create_short_url(db: Session, short_url: str, long_url: str) -> URL:
    """Creates and saves a new short URL entry in the database."""
    url = URL(short_url=short_url, long_url=long_url)
    db.add(url)
    db.commit()
    db.refresh(url)
    return url

def get_long_url(db: Session, short_url: str) -> URL | None:
    """Fetches the original long URL from the database using the short URL."""
    return db.query(URL).filter(URL.short_url == short_url).first()
