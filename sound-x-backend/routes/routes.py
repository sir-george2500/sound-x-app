# app/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import db_connection
from models.schemas.create_user_schema import UserCreate
from models.schemas.login_user_schema import UserLogin
from logic.register_and_login import register_new_user, login_user

router = APIRouter()

def get_db():
    db = db_connection()
    try:
        yield db
    finally:
        db.close()

@router.post("/user/register")
def create_user(user_data: UserCreate, session: Session = Depends(get_db)):
    try:
        # Use the register_new_user function from the logic module
        register_new_user(user_data, session)
        return {"message": "User created successfully"}
    except HTTPException as e:
        raise e

@router.post("/user/login")
def login(user_data: UserLogin, session: Session = Depends(get_db)):
    try:
        # Use the login_user function from the logic module
        response = login_user(user_data, session)
        return response
    except HTTPException as e:
        raise e
