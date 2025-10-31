from app.schemas.employee.employee_response import EmployeeResponse

class EmployeeWithManagerResponse(EmployeeResponse):
    manager : EmployeeResponse | None = None
    