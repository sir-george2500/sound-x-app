from fastapi import HTTPException
from passlib.context import CryptContext
from crud.crud import CRUD
from models.schemas.create_user_schema import UserCreate
from sqlalchemy.orm import Session

class UserValidator:
    def __init__(self, crud: CRUD, pwd_context: CryptContext):
        """
        Initializes a UserValidator instance.

        Args:
            crud (CRUD): An instance of the CRUD class.
            pwd_context (CryptContext): An instance of the CryptContext class for password hashing.
        """
        self.crud = crud
        self.pwd_context = pwd_context

    def validate_for_duplicate_user(self, session: Session, email: str):
        """
        Validates if a user with the given email already exists in the database.

        Args:
            session (Session): The database session.
            email (str): The email to check for duplication.

        Raises:
            HTTPException: If a user with the given email already exists, raises a 400 HTTPException.
        """
        # Check if user already exists
        existing_user = self.crud.get_user_by_email(session, email=email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")

    def validate_user_credentials(self, session: Session, email: str, password: str):
        """
        Validates user credentials (checks if the user exists and the password is correct).

        Args:
            session (Session): The database session.
            email (str): The user's email.
            password (str): The user's password.

        Raises:
            HTTPException: If the user does not exist or the password is incorrect, raises a 401 HTTPException.
        """
        # Check if user exists
        user = self.crud.get_user_by_email(session, email=email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        # Check if the password is correct
        if not self.pwd_context.verify(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        return user