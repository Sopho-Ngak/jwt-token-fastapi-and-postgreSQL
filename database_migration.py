from database import engine, Base
from app.user.models import User
Base.metadata.create_all(bind=engine)
