import random
import string

from sqlalchemy.orm import Session
from app.db.models import URL
from app.core.redis_client import redis_client

def generate_short_code(length: int = 6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def create_short_url(original_url: str, db: Session):
    short_code = generate_short_code()

    url = URL(
        original_url=str(original_url),
        short_code=short_code
    )    

    db.add(url)
    db.commit()
    db.refresh(url)

    return short_code

def get_original_url(short_code: str, db: Session):
    cached_url = redis_client.get(short_code)

    if cached_url:
        url = db.query(URL).filter(URL.short_code == short_code).first()
        if url:
            url.clicks += 1
            db.commit()

        return cached_url.decode()

    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        return None

    url.clicks += 1
    db.commit()

    redis_client.set(short_code, url.original_url)

    return url.original_url            