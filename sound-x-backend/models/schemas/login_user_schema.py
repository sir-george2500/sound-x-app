from pydantic import BaseModel, EmailStr, Field

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Invalid email address")
    password: str = Field(..., min_length=7, description="Password must be greater than 6 characters")


class ForgetPassword(BaseModel):
    email: EmailStr = Field(..., description="Invalid email address")
