from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import UserService
from app.services.employee_service import EmployeeService
from app.services.payroll_record_service import PayrollRecordService
from app.repositories.payroll_record_repository import PayrollRecordRepository
from app.services.files_service import FilesService
from app.services.mail_service import MailService
from app.repositories.user_repository import UserRepository
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.user.user_response import UserResponse
from app.utils.errors.CredentialsException import CredentialsException
from app.core.auth.jwt import oauth2_scheme
from app.core.logging import get_logger
from jose import jwt
from app.db.session import get_async_session
from app.core.config import get_settings

logger = get_logger(__name__)

SECRET_KEY = get_settings().jwt.SECRET_KEY.get_secret_value()
ALGORITHM = get_settings().jwt.ALGORITHM


async def get_user_service( 
    session: AsyncSession = Depends(get_async_session)
) -> UserService:
    repo = UserRepository(session)
    service = UserService(repo)
    return service

async def get_employee_service(
    session: AsyncSession = Depends(get_async_session)
) -> EmployeeService:
    repo = EmployeeRepository(session)
    service = EmployeeService(repo)
    return service

async def get_payroll_record_service(
    session: AsyncSession = Depends(get_async_session)
) -> PayrollRecordService:
    repo = PayrollRecordRepository(session)
    service = PayrollRecordService(repo)
    return service

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service=Depends(get_user_service)
) -> UserResponse:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    if not username:
        raise CredentialsException()
    user = await user_service.get_user_by_username(username)
    if not user:
        raise CredentialsException()
    return user


async def get_current_manager_user(
    user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    if "MANAGER" not in user.roles:
        raise CredentialsException()
    return user

async def get_file_service(
) -> FilesService:
    service = FilesService()
    return service

async def get_mail_service(
) -> MailService:
    service = MailService()
    return service