#!/usr/bin/env python3
from .auth import Auth
import uuid
"""SessionAuth class
"""

class SessionAuth(Auth):
    
    user_id_by_session_id = {}
    
    def create_session(self, user_id: str = None) -> str:
        """ Create session
        """
        if user_id == None or not isinstance(user_id, str):
            return None
        else:
            key = str(uuid.uuid4())
            self.user_id_by_session_id[key] = user_id
            return key
        
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ user id
        """
        if session_id == None or not isinstance(session_id, str):
            return None
        
        return self.user_id_by_session_id.get(session_id)
            