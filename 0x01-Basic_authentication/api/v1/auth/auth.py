#!/usr/bin/env python3
""" Auth module
"""

from flask import request
from typing import List, TypeVar

class Auth():
    """ Class Auth
    """
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require authentication function
        """
        if path == None:
            return True
        if not path.endswith('/'):
            path += '/'
        if path not in excluded_paths or excluded_paths == None:
            return True
        return False
    
    def authorization_header(self, request=None) -> str:
        """ Get authentication from requst header
        """
        if request is None:
            return None
        
        return request.headers.get('Authorization', None)
    
    def current_user(self, request=None) -> TypeVar('User'):
        """ Get currenet USER
        """
        return None