#!/usr/bin/env python3
from .auth import Auth
from models.user import User
import base64
"""BassiAuth class
"""

class BasicAuth(Auth):
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ Extract authenticatin header function
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        
        # Return the part of the header after "Basic "
        return authorization_header[len("Basic "):]
    
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ Decode authenticatin header function
        """
        if base64_authorization_header == None:
            return None
        
        if not isinstance(base64_authorization_header, str):
            return None
        
        try:
            decoded_string = base64.b64decode(base64_authorization_header).decode('utf-8')
            return decoded_string
        except:
            return None
        
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extact user credentials
        """
        if decoded_base64_authorization_header is None:
            return tuple(None, None)
        
        if not isinstance(decoded_base64_authorization_header, str):
            return tuple(None, None)
        
        if ':' not in decoded_base64_authorization_header:
            return tuple(None, None)
        
        return tuple(decoded_base64_authorization_header.split(':', 1))
    
    
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> User:
        """ Retrieve the User instance based on the provided credentials
        """
        if user_email is None or user_pwd is None:
            return None
        try:
            user_list = User.search({'email': user_email})
            if not user_list:
                return None
            user = user_list[0]
            if user.is_valid_password(user_pwd):
                return user
        except Exception:
            return None
        return None
    
    def current_user(self, request=None) -> User:
        """ Retrieve the current user based on the Authorization header
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if decoded_auth is None:
            return None
        user_email, user_pwd = self.extract_user_credentials(decoded_auth)
        if user_email is None or user_pwd is None:
            return None
        return self.user_object_from_credentials(user_email, user_pwd)