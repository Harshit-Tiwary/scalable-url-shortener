from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.core.rate_limiter import rate_limiter
from app.db.database import engine
from app.db.models import Base

app = FastAPI(title="Scalable URL Shortener")

# Create DB tables automatically
Base.metadata.create_all(bind=engine)

@app.middleware("http")
async def add_rate_limit(request: Request, call_next):

    # Skip rate limit for health
    if request.url.path == "/health":
        return await call_next(request)

    try:
        await rate_limiter(request)
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail},
        )

    response = await call_next(request)
    return response


app.include_router(router)