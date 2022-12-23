from database import engine, Base
from app.user.models import User
from app.posts.models import Post
Base.metadata.create_all(bind=engine)
