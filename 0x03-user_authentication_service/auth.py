#!/usr/bin/env python3
import bcrypt

def _hash_password(password: str) -> bytes:
        """Hash a password with bcrypt and return the salted hash.
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed