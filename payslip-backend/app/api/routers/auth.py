from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.schemas.user.user_create import UserCreate
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user.user_response import UserResponse
from app.api.deps import get_user_service
from fastapi import HTTPException
from app.core.config import get_settings
from datetime import timedelta
from app.core.auth.jwt import create_access_token
from app.core.logging import get_logger

logger = get_logger(__name__)

auth_router = APIRouter(prefix="/api/auth", tags=["auth"])

@auth_router.post('/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, user_service=Depends(get_user_service)):
    try:
        created_user = await user_service.create_user(user)
        return created_user
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error registering user")

@auth_router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                user_service=Depends(get_user_service)):
    try:
        authenticated_user = await user_service.authenticate_user(form_data.username, form_data.password)
        if not authenticated_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(get_settings().jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
        get_logger(__name__).info(f"User {authenticated_user.username} logged in successfully with roles {authenticated_user.roles}")
        access_token = create_access_token(
            data={"sub": str(authenticated_user.username), "roles": authenticated_user.roles, "email": authenticated_user.email},
            expires_delta=access_token_expires
        )
        get_logger(__name__).info(f"User {authenticated_user.username} logged in successfully")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error logging in user")
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"})