import asyncio
from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from app.schemas.payroll_record.payroll_record_response import PayrollRecordResponse
from app.api.deps import get_employee_service, get_payroll_record_service
from app.api.deps import get_current_manager_user, get_current_user
from app.schemas.date.date_request import DateRequest
from app.core.logging import get_logger
from idemptx.decorator import idempotent
from typing import List
from app.core.idempotency import async_redis_backend

payroll_record_router = APIRouter(prefix="/api/payrollRecord", tags=["payroll_record"])

@payroll_record_router.post("/generatePayrollReportsForEmployees")
@idempotent(storage_backend=async_redis_backend, key_ttl=600)
async def generate_payroll_reports_for_employees(date: DateRequest,
                                                 request: Request,
                                                 manager=Depends(get_current_manager_user),
                                                 employee_service=Depends(get_employee_service),
                                                 payroll_record_service=Depends(get_payroll_record_service)):
    try:
        employees_info = await employee_service.get_employees_ids_and_mails_by_manager_email(manager_email=manager.email)
        if not employees_info:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "No employees found"})

        report_tasks = []
        for emp_id, emp_email in employees_info:
            emp_payroll_data = await employee_service.get_employee_info_for_payroll(employee_email=emp_email, month=date.month, year=date.year)
            if not emp_payroll_data:
                get_logger(__name__).info(f"No payroll data found for employee ID: {emp_id}, creating payroll record.")
            report_tasks.append( payroll_record_service.generate_payroll_report(emp_payroll_data) )
  
        await asyncio.gather(*report_tasks)
        return JSONResponse(content={"detail": "Payroll reports generated successfully"})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": f"Error generating payroll reports: {str(e)}"})
    
@payroll_record_router.get("/myRecords", response_model=List[PayrollRecordResponse])
async def get_my_payroll_records(
    user=Depends(get_current_user),
    payroll_record_service=Depends(get_payroll_record_service)
):
    try:
        payroll_records = await payroll_record_service.get_by_employee_email(employee_email=user.email)
        return JSONResponse(content=[PayrollRecordResponse.model_validate(obj).model_dump() for obj in payroll_records])
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": f"Error fetching payroll records: {str(e)}"})


