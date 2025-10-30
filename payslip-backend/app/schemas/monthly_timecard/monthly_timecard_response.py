from app.schemas.monthly_timecard.monthly_timecard_base import MonthlyTimecardBase
from pydantic import Field
from app.schemas.employee.employee_response_manager import EmployeeResponseManager

class MonthlyTimecardResponse(MonthlyTimecardBase):
    employee: EmployeeResponseManager = Field(..., alias="employee")