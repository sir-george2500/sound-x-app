import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from models.models import CreateUser, Base
from models.schemas.create_user_schema import UserCreate
from crud.crud import CRUD

class TestCRUD(unittest.TestCase):
    def setUp(self):
        # Set up an in-memory SQLite database for testing
        engine = create_engine('sqlite:///:memory:')
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.db = SessionLocal()
        Base.metadata.create_all(bind=engine)
        self.crud = CRUD()

    def tearDown(self):
        # Close the database session and roll back any changes
        self.db.close()

    def test_create_user(self):
        # Create a UserCreate instance with test data
        user_create_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "user_role": "user",
        }
        user_create = UserCreate(**user_create_data)

        # Call the create_user method
        created_user = self.crud.create_user(self.db, user_create)

        # Assert that the user was created successfully
        self.assertIsInstance(created_user, CreateUser)
        self.assertEqual(created_user.username, "testuser")
        self.assertEqual(created_user.email, "test@example.com")

    def test_get_user_by_email(self):
        # Create a user in the database
        user_create_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "user_role": "user",
        }
        user_create = UserCreate(**user_create_data)
        created_user = self.crud.create_user(self.db, user_create)

        # Call the get_user_by_email method
        retrieved_user = self.crud.get_user_by_email(self.db, email="test@example.com")

        # Assert that the retrieved user matches the created user
        self.assertIsNotNone(retrieved_user)
        self.assertIsInstance(retrieved_user, CreateUser)
        self.assertEqual(retrieved_user.username, "testuser")
        self.assertEqual(retrieved_user.email, "test@example.com")

    def test_update_user(self):
        # Create a user in the database
        user_create_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "user_role": "user",
        }
        user_create = UserCreate(**user_create_data)
        created_user = self.crud.create_user(self.db, user_create)

        updated_data = {
            "username": "updateduser",
            "password": "updatedpassword",
        }
        updated_user = self.crud.update_user(self.db, email="test@example.com", **updated_data)

        # Assert that the user was updated successfully
        self.assertIsNotNone(updated_user)
        self.assertIsInstance(updated_user, CreateUser)
        self.assertEqual(updated_user.username, "updateduser")
        self.assertEqual(updated_user.password, "updatedpassword")

if __name__ == '__main__':
    unittest.main()


