
import uuid
from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

class UserTypeEnum(str, Enum):
    user = "user"
    admin = "admin"

class UserGenderEnum(str, Enum):
    male = "male"
    femmale = "femmale"
    other = "other"

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    full_name = Column(String(2500))
    phone_number = Column(String(2500), nullable=True)
    email = Column(String, unique=True, index=True)
    address = Column(String(2500), nullable=True)
    user_type = Column(Enum("user","admin", name="user type"), default=UserTypeEnum.user)
    gender = Column(Enum("male", "female", "other", name="User Gemder"), default=UserGenderEnum.other)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
