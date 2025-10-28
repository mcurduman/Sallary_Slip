from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorated(*args, **kwargs):
            claims = get_jwt()
            if claims['role'] != role:
                return jsonify({"msg": "Access denied"}), 403
            return fn(*args, **kwargs)
        return decorated
    return wrapper