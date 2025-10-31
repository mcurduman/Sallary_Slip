from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer
from app.schemas.user.user_create import UserCreate
from app.schemas.user.user_login import UserLogin
from app.schemas.user.user_response import UserResponse
from app.api.deps import get_user_service

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post('/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, user_service=Depends(get_user_service)):
    created_user = await user_service.create_user(user)
    return created_user

jwt = JwtAccessBearer(secret_key="your-secret-key")

@router.post('/login')
async def login(user: UserLogin, user_service=Depends(get_user_service)):
    authenticated_user = await user_service.authenticate_user(user)
    if authenticated_user:
        access_token = jwt.encode({
            "sub": str(authenticated_user.id),
            "role": authenticated_user.role,
            "email": authenticated_user.email
        })
        return JSONResponse(content={"access_token": access_token})
    return JSONResponse(content={"msg": "Bad username or password"}, status_code=401)

@router.post('/refresh')
async def refresh(credentials: JwtAuthorizationCredentials = Depends(jwt)):
    identity = credentials.subject
    access_token = jwt.encode({"sub": identity})
    return JSONResponse(content={"access_token": access_token})

@router.post('/logout')
async def logout():
    # JWT is stateless, so logout is handled client-side (delete token)
    return JSONResponse(content={"msg": "logout successful"})

@router.get('/me', response_model=UserResponse)
async def me(credentials: JwtAuthorizationCredentials = Depends(jwt), user_service=Depends(get_user_service)):
    identity = credentials.subject
    user = await user_service.get_user_by_id(identity)
    return user