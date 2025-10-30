from app.utils.errors.BaseAppException import BaseAppException
class ExternalServiceException(BaseAppException):
    """Raised when an external API or service fails"""
    def __init__(self, message: str = "External service unavailable"):
        super().__init__(message, status_code=502)
