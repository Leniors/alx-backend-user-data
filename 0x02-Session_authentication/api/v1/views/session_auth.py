#!/usr/bin/env python3
""" Module of Session views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_user() -> str:
    """ POST /api/v1/auth_session/login/
    """
    email = request.form.get('email')
    password = request.form.get('password')
    
    if email == None:
        return jsonify({ "error": "email missing" }), 400
    elif password == None:
        return jsonify({ "error": "password missing" }), 400
    
    users = User.search({'email': email})
    
    if not users:
        return jsonify({ "error": "no user found for this email" }), 404
    else:
        user = users[0]
        if not user.is_valid_password(password):
            return jsonify({ "error": "wrong password" }), 401
        
        from api.v1.app import auth
        
        session_id = auth.create_session(user.id)
        
        # Return the dictionary representation of the User
        response = jsonify(user.to_json())
        session_name = getenv('SESSION_NAME')
        response.set_cookie(session_name, session_id)

        return response
    
@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout_user(user_id: str = None) -> str:
    """ DELETE session
    """
    from api.v1.app import auth
    
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
