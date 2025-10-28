# from datetime import timedelta
# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import (
#     create_access_token,
#     create_refresh_token,
#     jwt_required,
#     get_jwt_identity,
#     set_access_cookies,
#     set_refresh_cookies,
#     unset_jwt_cookies,
# )
# app = Blueprint("auth", __name__)

# @app.route('/register', methods=['POST'])
# def register():
#     username = request.json.get('username')
#     password = request.json.get('password')
#     role = request.json.get('role')

#     if User.query.filter_by(username=username).first():
#         return jsonify({"msg": "User already exists"}), 400

#     new_user = User(username=username, password=password, role=role)
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({"msg": "User registered successfully"}), 201

# @app.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('username')
#     password = request.json.get('password')

#     user = User.query.filter_by(username=username, password=password).first()
#     if user:
#         access_token = create_access_token(identity={'username': user.username, 'role': user.role})
#         return jsonify(access_token=access_token), 200

#     return jsonify({"msg": "Bad username or password"}), 401