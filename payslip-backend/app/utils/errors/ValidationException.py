from app.utils.errors.BaseAppException import BaseAppException
class ValidationException(BaseAppException):
    """Raised when input validation fails"""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)