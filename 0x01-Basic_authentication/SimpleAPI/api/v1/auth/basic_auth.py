#!/usr/bin/env python3
from .auth import Auth

class BasicAuth(Auth):
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        if authorization_header is None:
            return None
        if isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        
        # Return the part of the header after "Basic "
        return authorization_header[len("Basic "):]