from typing import Any, Union
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config import settings
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from database import get_db
from app.user.schema import TokenData, UserOut
from app.user.models import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login",
    scheme_name="Bearer",
    )

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db))-> Union[UserOut, Any]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenData(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
                )
    except (jwt.JWTError, ValidationError):
        raise credentials_exception
    user = db.query(User).filter(User.username == payload.get("username")).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
            )
    return user