from app.utils.errors.DatabaseException import DatabaseException
class IntegrityConstraintException(DatabaseException):
    """Raised when a unique or foreign key constraint fails"""
    def __init__(self, message: str = "Integrity constraint violated"):
        super().__init__(message, status_code=400)