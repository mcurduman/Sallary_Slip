from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status
from app.utils.errors.BaseAppException import BaseAppException
from app.utils.errors.DatabaseException import DatabaseException
from app.utils.errors.ResourceNotFoundException import ResourceNotFoundException

def register_error_handlers(app):
    @app.exception_handler(BaseAppException)
    async def handle_app_error(request: Request, exc: BaseAppException):
        return JSONResponse(status_code=exc.status_code, content={"error": exc.message})

    @app.exception_handler(DatabaseException)
    async def handle_database_error(request: Request, exc: DatabaseException):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": "A database error occurred."})
    
    @app.exception_handler(ResourceNotFoundException)
    async def handle_not_found_error(request: Request, exc: ResourceNotFoundException):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": exc.message})

    import traceback
    @app.exception_handler(Exception)
    async def handle_generic_error(request: Request, exc: Exception):
        print("\n--- INTERNAL SERVER ERROR ---\n", traceback.format_exc(), "\n----------------------------\n")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": f"Internal server error: {str(exc)}"})