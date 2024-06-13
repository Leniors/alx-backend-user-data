#!/usr/bin/env python3
""" Flask app
"""
from flask import Flask, jsonify, request
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
    
    # if not email or not password:
    #     return jsonify({"message": "email and password required"}), 400

    try:
        user = AUTH.register_user(email=email, password=password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")