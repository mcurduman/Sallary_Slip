from app.schemas.employee.employee_base import EmployeeBase
from app.utils.validators.national_id_validator import validate_national_id
from pydantic import method_validator

class EmployeeCreate(EmployeeBase):
    @method_validator(mode="after")
    def validate_national_id(self):
        result = validate_national_id(self.national_id, self.country_of_id)
        if result is not True:
            raise ValueError("National ID validation failed: " + result)
        return self