from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr,Field

class UserCreate(BaseModel):
    username: str = Field(..., mid_length=7, description="Invalid Email")
    email: EmailStr = Field(..., description="Invalid email address")
    password: str = Field(..., min_length=7, description="Password must be greater than 6 characters")
    user_role: Optional[str] = None
    forget_password_token: Optional[str] = None
    forget_password_token_expiry: Optional[datetime] = None
    verify_user_token: Optional[str] = None
    verify_user_token_expiry: Optional[datetime] = None
    profile_picture: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "sample_username",
                "email": "sample@example.com",
                "password": "sample_password",
                "user_role": "sample_role",
                "forget_password_token": "sample_token",
                "forget_password_token_expiry": "2023-01-01T12:00:00",
                "verify_user_token": "sample_verify_token",
                "verify_user_token_expiry": "2023-01-01T12:00:00",
                "profile_picture": "sample_picture",
            }
        }