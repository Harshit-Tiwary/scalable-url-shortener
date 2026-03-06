from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.url import URLCreate, URLResponse
from app.services.url_service import create_short_url, get_original_url
from app.db.models import URL

router = APIRouter()


@router.post("/shorten", response_model=URLResponse)
def shorten_url(payload: URLCreate, db: Session = Depends(get_db)):
    short_code = create_short_url(payload.original_url, db)

    return {
        "short_url": f"http://localhost:8000/{short_code}"
    }


@router.get("/stats/{short_code}", response_model=dict)
def get_stats(short_code: str, db: Session = Depends(get_db)):

    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    return {
            "short_code": url.short_code,
            "original_url": url.original_url,
            "clicks": url.clicks
    }

@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):

    url = db.query(URL).filter(URL.short_code == short_code).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    url.clicks += 1
    db.commit()

    return RedirectResponse(url.original_url) 