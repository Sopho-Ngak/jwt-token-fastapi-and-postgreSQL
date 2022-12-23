from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.user.routes import router as user_router
from app.posts.routes import router as post_router
from database import engine, Base
from app.user.models import User
app = FastAPI(title="JWT Token authentication using PostgreSQL", version="0.1.0", docs_url="/api/v1/docs", redoc_url="/api/v1/redoc")

app.include_router(user_router, prefix="/users", tags=["User"])
app.include_router(post_router, prefix="/posts", tags=["Post"])

@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/api/v1/docs')