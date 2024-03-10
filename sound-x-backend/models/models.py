# models.py
from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CreateUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String)
    user_role = Column(String, nullable=True)
    forget_password_token = Column(String, nullable=True)
    forget_password_token_expiry = Column(DateTime(timezone=True), nullable=True)
    verify_user_token = Column(String, nullable=True)
    verify_user_token_expiry = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_email_verified = Column(Boolean, default=False)
    profile_picture = Column(String, nullable=True)
