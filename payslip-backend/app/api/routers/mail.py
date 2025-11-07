from io import BytesIO
import base64
from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from app.api.deps import get_employee_service, get_payroll_record_service, get_file_service, get_mail_service
from app.api.deps import get_current_manager_user
from app.schemas.date.date_request import DateRequest
from idemptx.decorator import idempotent
from app.schemas.email.recipient import Recipient
from datetime import date as date_func
from app.core.logging import get_logger
from app.core.idempotency import async_redis_backend
from datetime import datetime

mail_router = APIRouter(prefix="/api/mail", tags=["mail"])

@mail_router.post("/sendPayslips")
@idempotent(storage_backend=async_redis_backend, key_ttl=600)
async def send_payslips(date: DateRequest,
                        request: Request,
                        manager=Depends(get_current_manager_user),
                        employee_service=Depends(get_employee_service),
                        mail_service=Depends(get_mail_service),
                        payroll_record_service=Depends(get_payroll_record_service),
                        file_service=Depends(get_file_service)):
    try:
        employees_info = await employee_service.get_employees_ids_and_mails_by_manager_email(manager_email=manager.email)
        if not employees_info:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "No employees found"})

        emp_ids = [emp_id for emp_id, _ in employees_info]
        employees_mails = [{"employee_id": emp_id, "employee_email": emp_email} for emp_id, emp_email in employees_info]
        get_logger(__name__).info(f"Employee mails mapping: {employees_mails}")
        payroll_records = await payroll_record_service.get_all_by_ids(emp_ids, month=date.month, year=date.year)
        if not payroll_records:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "No payroll records found for the specified month and year"})

        recipients = []
        for payroll_record in payroll_records:
            filename = f"Payslip_{payroll_record.employee_full_name}_{payroll_record.payroll_month}_{payroll_record.payroll_year}.pdf"
            file = file_service.render_payslip_pdf(payroll_record, filename=filename)

            employee_email = next((emp["employee_email"] for emp in employees_mails if emp["employee_id"] == payroll_record.employee_id), None)
            pdf_b64 = base64.b64encode(file).decode('utf-8')
            recipients.append(Recipient(email=employee_email,
                                        name=payroll_record.employee_full_name,
                                        pdf_b64=pdf_b64))
            filename = f"employee_report_{manager.email}_{date.month}_{date.year}.csv"
            destination_folder = "manager_reports"
            await file_service.save_upload_file(buffer=BytesIO(file), filename=filename, destination_folder=destination_folder)
            
        mail_service.send_batch_email(
            month=date.month,
            sent_date=date_func.today().strftime("%d %B %Y"),
            recipients=recipients
        )
        return JSONResponse(content={"detail": "Payroll reports generated successfully"})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": f"Error generating payroll reports: {str(e)}"})

@mail_router.post("/sendAggregatedEmployeeData")
@idempotent(storage_backend=async_redis_backend, key_ttl=600)
async def send_employee_report(date: DateRequest,
                                request: Request,
                               file_service=Depends(get_file_service),
                                mail_service=Depends(get_mail_service),
                                manager=Depends(get_current_manager_user)):
    try:
        file_path = f"manager_reports/employee_report_{manager.email}_{date.month}_{date.year}.csv"
        file = await file_service.get_file_content(file_path)
        if file is None:
            return JSONResponse(status_code=404, content={"detail": "Report file not found. Please generate the report first."})
        mail_service.send_single_email(
            manager_email=manager.email,
            name=f"{manager.username}",
            sent_date=f"{date.year}-{date.month}-01",
            month=datetime(year=date.year, month=date.month, day=1).strftime("%B %Y"),
            file=file
        )
        return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "Report generated and saved successfully"})
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Error generating report"})
