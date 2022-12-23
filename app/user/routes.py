from fastapi import APIRouter, Depends, HTTPException, status, Body
from .schema import UserOut, UserCreate, UserUpdate, TokenData,TokenSheman, UserLogin
from sqlalchemy.orm import Session
from database import get_db
from .models import User as UserModel
from utils.auth import (get_password_hash, verify_password, create_access_token, create_refresh_token)
from utils.dependencies import get_current_user
import uuid
from datetime import datetime
from jose import jwt
from config import settings
from typing import Any

router = APIRouter()

@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(UserModel).filter(UserModel.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(UserModel).filter(UserModel.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    if db.query(UserModel).filter(UserModel.phone_number == user.phone_number).first():
        raise HTTPException(status_code=400, detail="Phone number already exists")
    user.hashed_password = get_password_hash(user.hashed_password)
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=TokenSheman)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if not db_user:
        db_user = db.query(UserModel).filter(UserModel.email == user.username).first()
        if not db_user:
            db_user = db.query(UserModel).filter(UserModel.phone_number == user.username).first()
            if not db_user:
                raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(user.hashed_password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    data = {
        "username": db_user.username,
        "full_name": db_user.full_name,
        "phone_number": db_user.phone_number,
        "email": db_user.email,
        "address": db_user.address,
        "user_type": db_user.user_type,
    }
    access_token = create_access_token(data=data)
    refresh_token = create_refresh_token(data=data)
    return {"access_token": str(access_token), "refresh_token": str(refresh_token)}

@router.post("/refresh", response_model=TokenSheman)
def refresh(refresh_token: Any=Body(), db: Session = Depends(get_db)):
    refresh_token = refresh_token.get("refresh_token")
    try:
        payload = jwt.decode(str(refresh_token), settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenData(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Login required",
                headers={"WWW-Authenticate": "Bearer"},
                )
        db_user = db.query(UserModel).filter(UserModel.username == payload.get("username")).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User has been deleted")
        access_token = create_access_token(data=payload)
        return {
            "access_token": str(access_token),
            "refresh_token": str(refresh_token)}
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid refresh token", 
            headers={"WWW-Authenticate": "Bearer"})

    


@router.get("/me", response_model=UserOut)
def me(user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    return user

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: uuid.UUID, current_user: UserModel=Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.get("/", response_model=list[UserOut])
def get_users(current_user: UserModel=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(UserModel).all()