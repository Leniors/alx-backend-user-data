#!/usr/bin/env python3
""" Flask app
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

app = Flask(__name__)

AUTH = Auth()

@app.route("/", methods=['GET'])
def root():
    """ root route
    """
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=['POST'])
def create_user():
    """ create user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        user = AUTH.register_user(email=email, password=password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

@app.route('/sessions', methods=['POST'])
def login():
    """Login user and create a new session
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)

    if not AUTH.valid_login(email, password):
        abort(401)
    # Assuming there is a method to create a session for the user
    user = AUTH._db.find_user_by(email=email)
    session_id = AUTH.create_session(email)  # Create session ID for the user
    print(session_id)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response

@app.route('/sessions', methods=['DELETE'])
def logout():
    """Log out a user by destroying their session."""
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    response = make_response(redirect("/"))
    response.set_cookie("session_id", "", expires=0)
    return response

@app.route('/profile', methods=['GET'])
def profile():
    """Get user profile by session ID.
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        return abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        return abort(403)

    return jsonify({"email": user.email}), 200

@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """Handles the POST /reset_password route to generate a reset token.
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"message": "Email is required"})

    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        return jsonify({"message": "Email not registered"}), 403
    
@app.route('/reset_password', methods=['PUT'])
def update_password():
    """Handles the PUT /reset_password route to update user's password.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        return jsonify({"message": "Email, reset_token, and new_password are required"})

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        return jsonify({"message": "Invalid reset token"}), 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")