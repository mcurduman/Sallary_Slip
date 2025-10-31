from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.utils.errors.BaseAppException import BaseAppException

def register_error_handlers(app):
    @app.exception_handler(BaseAppException)
    async def handle_app_error(request: Request, exc: BaseAppException):
        return JSONResponse(status_code=exc.status_code, content={"error": exc.message})

    @app.exception_handler(IntegrityError)
    async def handle_integrity_error(request: Request, exc: IntegrityError):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "Integrity constraint violated"})

    @app.exception_handler(SQLAlchemyError)
    async def handle_sqlalchemy_error(request: Request, exc: SQLAlchemyError):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Database error"})

    @app.exception_handler(Exception)
    async def handle_generic_error(request: Request, exc: Exception):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "Internal server error"})