#!/usr/bin/env python3
""" Auth module
"""

import fnmatch
from typing import List, TypeVar

class Auth():
    """ Class Auth
    """
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require authentication function
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        # Ensure path ends with a slash for consistent comparison
        if not path.endswith('/'):
            path += '/'

        # Iterate over each pattern in excluded_paths
        for pattern in excluded_paths:
            # Ensure pattern ends with a slash for consistent comparison
            if not pattern.endswith('/'):
                pattern += '/'
            # Use fnmatch to match the path with the pattern
            if fnmatch.fnmatch(path, pattern):
                return False
        return True
    
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