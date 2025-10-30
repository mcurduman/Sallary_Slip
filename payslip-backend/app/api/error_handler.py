from flask import Flask, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.utils.errors.BaseAppException import BaseAppException

def register_error_handlers(app: Flask):
    @app.errorhandler(BaseAppException)
    def handle_app_error(exc: BaseAppException):
        return jsonify({"error": exc.message}), exc.status_code

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(exc: IntegrityError):
        return jsonify({"error": "Integrity constraint violated"}), 400

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(exc: SQLAlchemyError):
        return jsonify({"error": "Database error"}), 500

    @app.errorhandler(Exception)
    def handle_generic_error(exc: Exception):
        return jsonify({"error": "Internal server error"}), 500