from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from config.db import db_connection
from models.schemas.create_user_schema import UserCreate
from models.schemas.login_user_schema import UserLogin
from validator.user_validator import UserValidator
from crud.crud import CRUD
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import jwt
import random
import string

# Load environment variables from .env file
load_dotenv()

# Create an instance of the CRUD class
crud = CRUD()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_validator = UserValidator(crud=crud, pwd_context=pwd_context)

# Access environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def register_new_user(user_data: UserCreate, session: Session = Depends(db_connection)):
    """
    Register a new user, handling validation, password hashing, and database operations.

    Args:
        user_data (UserCreate): User creation data.
        session (Session): The database session.

    Raises:
        HTTPException: If validation, password hashing, or user creation fails.
    """
    try:
        # Validate user data for duplication using the UserValidator
        user_validator.validate_for_duplicate_user(session, email=user_data.email)

        # Hash the user's password using the UserValidator
        hashed_password = pwd_context.hash(user_data.password)
        # Update the user_data with the hashed password
        user_data.password = hashed_password

        # Use the create_user method from the CRUD class
        crud.create_user(session, user_data)
    except HTTPException as e:
        # If an HTTPException occurs during validation, password hashing, or user creation, re-raise it
        raise e

def create_access_token(data: dict):
    to_encode = data.copy()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def login_user(user_data: UserLogin, session: Session = Depends(db_connection)):
    """
    Login a user, validate credentials, and create an access token.

    Args:
        user_data (UserLogin): User login credentials.
        session (Session): The database session.

    Returns:
        dict: A dictionary containing the access token.
    """
    try:
        # Validate user credentials
        user = user_validator.validate_user_credentials(session, email=user_data.email, password=user_data.password)

        # Create an access token
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        # If an HTTPException occurs during validation or login, re-raise it
        raise e

