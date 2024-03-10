import unittest
from unittest.mock import Mock
from fastapi import HTTPException
from validator.user_validator import UserValidator
from crud.crud import CRUD
from sqlalchemy.orm import Session
from passlib.context import CryptContext

class TestUserValidator(unittest.TestCase):
    def setUp(self):
        self.crud_mock = Mock(spec=CRUD)
        self.pwd_context_mock = Mock(spec=CryptContext)
        self.validator = UserValidator(crud=self.crud_mock, pwd_context=self.pwd_context_mock)

    def test_validate_for_duplicate_user_user_exists(self):
        # Mock the get_user_by_email method to return a user, indicating that the user already exists
        self.crud_mock.get_user_by_email.return_value = Mock()

        # Call the method being tested and expect an HTTPException with status_code 400
        with self.assertRaises(HTTPException) as context:
            self.validator.validate_for_duplicate_user(Mock(spec=Session), email="test@example.com")

        # Assert that the exception has the correct status_code and detail
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "User with this email already exists")

    def test_validate_for_duplicate_user_user_does_not_exist(self):
        # Mock the get_user_by_email method to return None, indicating that the user does not exist
        self.crud_mock.get_user_by_email.return_value = None

        # Call the method being tested with a non-existing user
        try:
            self.validator.validate_for_duplicate_user(Mock(spec=Session), email="test@example.com")
        except HTTPException as e:
            self.fail(f"HTTPException raised unexpectedly: {e}")

        # Optionally, add an assertion to ensure that the create_user method is not called
        self.crud_mock.create_user.assert_not_called()

    def test_validate_user_credentials_valid_credentials(self):
        # Mock the get_user_by_email method to return a user
        user_mock = Mock()
        user_mock.password = "hashed_password"
        self.crud_mock.get_user_by_email.return_value = user_mock

        # Mock the verify method to return True, indicating a valid password
        self.pwd_context_mock.verify.return_value = True

        # Call the method being tested with valid credentials
        try:
            self.validator.validate_user_credentials(
                Mock(spec=Session),
                email="test@example.com",
                password="valid_password",
            )
        except HTTPException as e:
            self.fail(f"HTTPException raised unexpectedly: {e}")

    def test_validate_user_credentials_invalid_credentials(self):
        # Mock the get_user_by_email method to return a user
        user_mock = Mock()
        user_mock.password = "hashed_password"
        self.crud_mock.get_user_by_email.return_value = user_mock

        # Mock the verify method to return False, indicating an invalid password
        self.pwd_context_mock.verify.return_value = False

        # Call the method being tested with invalid credentials and expect an HTTPException with status_code 401
        with self.assertRaises(HTTPException) as context:
            self.validator.validate_user_credentials(
                Mock(spec=Session),
                email="test@example.com",
                password="invalid_password",
            )

        # Assert that the exception has the correct status_code and detail
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Invalid password")


if __name__ == "__main__":
    unittest.main()
