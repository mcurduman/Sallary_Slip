from app.schemas.employee.employee_response import EmployeeResponse
from typing import List, Optional
class ManagerEmployeeResponse(EmployeeResponse):
    employees : Optional[List[EmployeeResponse]] = None
    