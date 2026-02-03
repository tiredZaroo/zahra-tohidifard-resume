

from sqlalchemy import Column, Integer, String
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    description = Column(String)
    budget = Column(Integer, default=0)
    deadline = Column(String, default="")


# from pydantic import BaseModel, EmailStr
# from typing import Optional
# from datetime import datetime

# class ProjectRequest(BaseModel):
#     name: str
#     email: EmailStr
#     project_type: str  # نوع پروژه: وب‌سایت، اپ موبایل، دسکتاپ، etc.
#     budget: str  # بودجه: کم، متوسط، بالا
#     timeline: str  # زمان‌بندی: فوری، 1-3 ماه، بیش از 3 ماه
#     description: str
#     phone: Optional[str] = None
#     company: Optional[str] = None
    
# class ProjectRequestDB(ProjectRequest):
#     id: str
#     status: str = "new"  # new, in_review, approved, rejected
#     created_at: datetime
#     ip_address: Optional[str] = None


# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class ProjectStatus(str, enum.Enum):
    NEW = "new"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"

class UserSession(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class ProjectRequest(Base):
    __tablename__ = "project_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20))
    company = Column(String(100))
    project_type = Column(String(50), nullable=False)
    budget = Column(String(30), nullable=False)
    timeline = Column(String(30), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(20), default=ProjectStatus.NEW, nullable=False)
    ip_address = Column(String(45))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AdminUser(Base):
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class OnlineUser(Base):
    __tablename__ = "online_users"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, nullable=False)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    page_url = Column(String(255))
    last_seen = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default=UserSession.ACTIVE)