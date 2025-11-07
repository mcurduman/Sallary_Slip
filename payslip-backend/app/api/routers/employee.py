from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from app.schemas.employee.employee_response import EmployeeResponse
from app.api.deps import get_employee_service
from app.api.deps import get_file_service
from app.api.deps import get_current_manager_user, get_current_user
from app.schemas.date.date_request import DateRequest
from fastapi.responses import StreamingResponse
from app.core.logging import get_logger
from idemptx.decorator import idempotent
from typing import List
from app.schemas.employee.employee_details import EmployeeDetails
from app.core.idempotency import async_redis_backend



logger = get_logger(__name__)

employee_router = APIRouter(prefix="/api/employee", tags=["employee"])

@employee_router.get("/all", response_model=List[EmployeeResponse], dependencies=[Depends(get_current_manager_user)])
async def get_all_employees(employee_service=Depends(get_employee_service)):
    try:
        employees = await employee_service.get_all_employees()
        return JSONResponse(content=[resp.model_dump(mode="json") for resp in employees])
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Error fetching employees"})
    
@employee_router.get("/byManager", dependencies=[Depends(get_current_manager_user)])
async def get_employees_by_email(
                              request: Request,
                              manager = Depends(get_current_manager_user),                
                              employee_service=Depends(get_employee_service)):
    try:
        logger.info(f"Fetching employees for manager: {manager.email}")
        employees = await employee_service.get_employees_details_by_manager_email(manager_email=manager.email)
        if not employees:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Employees not found"})
        logger.info(f"Fetched employees for manager {manager.email}: {employees}")
        return JSONResponse(content=[resp.dict(by_alias=True) for resp in employees])
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": f"Error fetching employee: {str(e)}"})

@employee_router.post("/createAggregatedEmployeeData")
@idempotent(storage_backend=async_redis_backend, key_ttl=600)
async def get_employee_by_email(date: DateRequest,
                                request: Request,
                                employee_service=Depends(get_employee_service),
                                file_service=Depends(get_file_service),
                                manager=Depends(get_current_manager_user)):
    try:
        logger.info(f"Fetching employee data for manager: {manager.email}, date: {date.month}/{date.year}")
         
        employees = await employee_service.get_employees_info_by_manager_email(manager_email=manager.email, month=date.month, year=date.year)
        if not employees:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "No employees found"})
        file = await file_service.employees_info_to_csv_file(employees)
        filename = f"employee_report_{manager.email}_{date.month}_{date.year}.csv"
        destination_folder = "manager_reports"
        await file_service.save_upload_file(buffer=file, filename=filename, destination_folder=destination_folder)
        return StreamingResponse(file, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={filename}"})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": f"Error fetching employees: {str(e)}"})
    
@employee_router.get("/getMyDetails", response_model=EmployeeDetails)
async def get_my_details(request: Request, employee_service=Depends(get_employee_service), user=Depends(get_current_user)):
    try:
        logger.info(f"Fetching details for employee: {user.email}")
        employee = await employee_service.get_employee_details_by_email(email=user.email)
        if not employee:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Employee not found"})
        logger.info(f"Fetched details for employee {user.email}: {employee}")
        return JSONResponse(content=employee.dict(by_alias=True))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": f"Error fetching employee details: {str(e)}"})