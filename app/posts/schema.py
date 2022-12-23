import uuid
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union, Any
from app.user.schema import UserOut


class PostBase(BaseModel):
    id: Union[uuid.UUID, None] = None
    title: str
    content: str
    author_id: Union[uuid.UUID, None] = None

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass

class PostOut(PostBase):
    author: Union[UserOut, None] = None

    class Config:
        orm_mode = True

class PostUpdate(BaseModel):
    title: Union[str, None] = None
    content: Union[str, None] = None

    class Config:
        orm_mode = True