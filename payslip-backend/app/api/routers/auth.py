from datetime import timedelta
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
## Removed unused UserResponse import
from app.schemas.user.user_create import UserCreate
from app.schemas.user.user_login import UserLogin
from app.api.deps import get_user_service

auth = Blueprint("api/auth", __name__)

@auth.route('/register', methods=['POST'])
def register():
    user = UserCreate(**request.get_json())
    created_user = get_user_service().create_user(user)
    return jsonify(created_user), 201

@auth.route('/login', methods=['POST'])
def login():
    user = UserLogin(**request.get_json())
    authenticated_user = get_user_service().authenticate_user(user)
    if authenticated_user:
        access_token = create_access_token(
            identity=str(authenticated_user.id),
            additional_claims={"role": authenticated_user.role,
                              "email": authenticated_user.email},
            expires_delta=timedelta(minutes=15)
        )
        refresh_token = create_refresh_token(
            identity=str(authenticated_user.id),
            expires_delta=timedelta(days=30)
        )
        response = jsonify({"login": True})
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response, 200
    return jsonify({"msg": "Bad username or password"}), 401

@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    response = jsonify(access_token=access_token)
    set_access_cookies(response, access_token)
    return response, 200

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response, 200

@auth.route('/me', methods=['GET'])
@jwt_required()
def me():
    identity = get_jwt_identity()
    user = get_user_service().get_user_by_id(identity['id'])
    return jsonify(user)