#!/usr/bin/env python3
""" Flask app
"""
from flask import Flask, jsonify, request, abort, make_response
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

    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")