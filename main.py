from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.user.routes import router as user_router
from database import engine, Base
from app.user.models import User
app = FastAPI(title="JWT Token authentication using PostgreSQL", version="0.1.0")

app.include_router(user_router, prefix="/users", tags=["User"])

@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')