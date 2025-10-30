from app.utils.errors.BaseAppException import BaseAppException

class UnauthorizedException(BaseAppException):
    """Raised when user is not authorized"""
    def __init__(self, message: str):
        super().__init__(message, status_code=401)