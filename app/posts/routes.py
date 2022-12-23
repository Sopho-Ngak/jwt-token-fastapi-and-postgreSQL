import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Body
from .schema import PostBase, PostOut, PostUpdate, PostCreate
from sqlalchemy.orm import Session
from database import get_db
from .models import Post as PostModel
from utils.dependencies import get_current_user
from app.user.models import User

router = APIRouter()

@router.post("/create", response_model=PostOut)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post.author_id = current_user.id
    db_post = PostModel(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/", response_model=list[PostOut])
def get_all_post(db: Session = Depends(get_db)):
    db_post = db.query(PostModel).all()
    if not db_post:
        raise HTTPException(status_code=404, detail="No post found")
    return db_post

@router.get("/get/{id}", response_model=PostOut)
def get_post(id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_post = db.query(PostModel).filter(PostModel.id == id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.put("/update/{id}", response_model=PostOut)
def update_post(id: uuid.UUID, post: PostUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):


    db_post = db.query(PostModel).filter(PostModel.id == id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to update this post")

    if post.title:
        db_post.title = post.title
    if post.content:
        db_post.content = post.content
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/delete/{id}")
def delete_post(id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_post = db.query(PostModel).filter(PostModel.id == id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this post")

    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully",
            "post title": db_post.title,
            "post author name": db_post.author.username,}