#!/usr/bin/env python3
""" class Auth
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hash a password with bcrypt and return the salted hash."""
        import bcrypt
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed

    def register_user(self, email: str, password: str) -> User:
        """Register a new user and return the User object."""
        try:
            # Check if the user already exists
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If no user found, proceed to create a new one
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user