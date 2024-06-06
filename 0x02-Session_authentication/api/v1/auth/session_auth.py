#!/usr/bin/env python3
from .auth import Auth
import uuid
"""SessionAuth class
"""

class SessionAuth(Auth):
    
    user_id_by_session_id = {}
    
    def create_session(self, user_id: str = None) -> str:
        """ Create session"""
        if user_id == None or not isinstance(user_id, str):
            return None
        else:
            key = str(uuid.uuid4())
            self.user_id_by_session_id[key] = user_id
            return key
            