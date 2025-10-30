from app.schemas.employee.employee_response import EmployeeResponse

class EmployeeResponseManager(EmployeeResponse):
    manager : EmployeeResponse | None = None