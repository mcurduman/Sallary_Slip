from fastapi import Depends, HTTPException, status
from app.api.deps import get_user_service
from functools import wraps
from app.core.logging import get_logger
logger = get_logger(__name__)

def roles_required(*roles):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user=Depends(get_user_service), **kwargs):
            if not any(role in current_user.roles for role in roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to access this resource"
                )
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator