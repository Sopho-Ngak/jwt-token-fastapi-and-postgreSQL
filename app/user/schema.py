import uuid
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union, Any
from .models import UserTypeEnum, UserGenderEnum

class UserBase(BaseModel):
    id : Union[uuid.UUID, None] = None 
    username : str 
    full_name : str 
    phone_number : Union[str, None] = None
    email : EmailStr 
    address : Optional[str] = None
    user_type : Union[UserTypeEnum, None] = None
    gender : Union[UserGenderEnum, None] = None
    hashed_password : str 

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    pass

class UserOut(BaseModel):
    id : Union[uuid.UUID, None] = None
    username : str 
    full_name : str
    phone_number : Union[str, None] = None
    email : EmailStr 
    address : Union[str, None] = None
    user_type : Union[UserTypeEnum, Any]
    gender : Union[UserGenderEnum, Any]

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    full_name : Optional[str] = Field(None, alias="Full Name")
    phone_number : Optional[str] = Field(None, alias="Phone Number")
    email : Optional[EmailStr] = Field(None, alias="Email")
    address : Optional[str] = Field(None, alias="Address")
    user_type : Optional[UserTypeEnum] = Field(None, alias="User Type")
    hashed_password : Optional[str] = Field(None, alias="Password")

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username : str 
    hashed_password : str

    class Config:
        orm_mode = True

class TokenSheman(BaseModel):
    access_token : str 
    refresh_token : str 

class TokenData(BaseModel):
    sub : str = None
    exp: int = None