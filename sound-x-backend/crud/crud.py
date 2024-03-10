from sqlalchemy.orm import Session
from models.models import CreateUser  # Assuming CreateUser is the model from models.py
from models.schemas.create_user_schema import UserCreate


class CRUD:
    """Handles create, read, update, and delete (CRUD) operations for users."""

    def create_user(self, db: Session, user_create: UserCreate) -> CreateUser:
        """Creates a new user in the database.

        Args:
            db: The database session.
            user_create: A UserCreate schema instance containing user data.

        Returns:
            The newly created user object.
        """

        user_data = user_create.model_dump()  # Extract data as a dictionary
        user = CreateUser(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_user_by_email(self, db: Session, email: str) -> CreateUser:
        """Gets a user by their email from the database.

        Args:
            db: The database session.
            email: The email of the user to retrieve.

        Returns:
            The user object if found, None otherwise.
        """
        return db.query(CreateUser).filter(CreateUser.email == email).first()

    def update_user(self, db: Session, email: str, **kwargs) -> CreateUser:
        """Updates a user's fields based on their email.

        Args:
            db: The database session.
            email: The email of the user to update.
            **kwargs: The fields to update with their new values.

        Returns:
            The updated user object.

        Raises:
            ValueError: If the user with the specified email is not found.
        """

        user = self.get_user_by_email(db, email)

        if user:
            for field, value in kwargs.items():
                setattr(user, field, value)
            db.add(user)
            db.commit()
            db.refresh(user)  # Refresh to get updated values
            return user
        else:
            raise ValueError(f"User with email '{email}' not found.")
