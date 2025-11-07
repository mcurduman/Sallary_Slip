from app.db.models.employee import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee.employee_response import EmployeeResponse
from typing import Optional, Iterable
from app.schemas.employee.emp_info import EmployeeInfo
import uuid
from app.utils.errors.DatabaseException import DatabaseException
from app.utils.errors.ResourceNotFoundException import ResourceNotFoundException
from app.utils.errors.BaseAppException import BaseAppException
from app.schemas.payroll_record.payroll_record_create import PayrollRecordCreate
from app.core.logging import get_logger
from app.schemas.employee.employee_details import EmployeeDetails
class EmployeeService:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    def _employee_to_response(self, employee: Employee) -> EmployeeResponse:
        return EmployeeResponse.model_validate({
            **employee.__dict__,
            "position": employee.position.title,
            "discipline": employee.discipline.name
        })

    async def create_employee(self, employee: Employee) -> Employee:
        try:
            created_employee = await self.employee_repository.create(employee)
            return self._employee_to_response(created_employee)
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to create employee: {str(e)}")
        
    async def get_employee_by_email(self, email: str
        ) -> Optional[Employee]:
        try:
            employee = await self.employee_repository.get_by_email(email)
            if not employee:
                return None
            return employee
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve employee: {str(e)}")
        
    async def get_all_employees(self) -> Iterable[EmployeeResponse]:
        try:
            employees = await self.employee_repository.get_all()
            response = [self._employee_to_response(emp) for emp in employees]
            return response
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve employees: {str(e)}")
        
    async def delete_employee(self, employee_id: uuid.UUID) -> None:
        try:
            await self.employee_repository.delete(employee_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to delete employee: {str(e)}")
        
    async def update_employee(self, employee: Employee
        ) -> Employee:
        try:
            return await self.employee_repository.update(employee)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to update employee: {str(e)}")

    async def is_manager(self, employee_id: uuid.UUID) -> bool:
        try:
            return await self.employee_repository.is_manager(employee_id)
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to check if employee is a manager: {str(e)}")
        
    async def get_managers(self) -> Iterable[Employee]:
        try:
            managers = await self.employee_repository.get_managers()
            return [self._employee_to_response(emp) for emp in managers]
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve managers: {str(e)}")

    async def get_employee_details_by_email(self, email: str) -> EmployeeDetails:
        try:
            employee_details = await self.employee_repository.get_employee_details_by_email(email)
            if not employee_details:
                raise ResourceNotFoundException("Employee details not found for the given email")
            return employee_details
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve employee details by email: {str(e)}")
        
    async def get_employees_details_by_manager_email(self, manager_email: str) -> Iterable[EmployeeDetails]:
        try:
            employee_details = await self.employee_repository.get_employees_details_by_manager_email(manager_email)
            get_logger(__name__).info(f"Employee details retrieved: {employee_details}")
            return employee_details
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve employee details by manager email: {str(e)}")

    async def get_employees_ids_and_mails_by_manager_email(self, manager_email: str) -> Iterable[uuid.UUID]:
        try:
            employees = await self.employee_repository.get_employees_ids_and_mails_by_manager_email(manager_email)
            if not employees:
                raise ResourceNotFoundException("No employees found for the given manager email")
            return employees
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve employee IDs by manager email: {str(e)}")
        
    async def get_employees_info_by_manager_email(self, manager_email: str, month: int, year: int):
        try:
            results =  await self.employee_repository.get_by_manager_email(manager_email, month, year)
            if not results:
                raise ResourceNotFoundException("No employees found for the given manager email")
            response = []
            for employee in results:
                response.append(EmployeeInfo(
                    full_name=f"{employee['employee'].first_name} {employee['employee'].last_name}",
                    email=employee['employee'].email,
                    gross_salary=sum([pr.employee_base_salary for pr in employee["payroll_records"]]),
                    net_salary=sum([pr.employee_net_salary for pr in employee["payroll_records"]]),
                    working_days=sum([tc.worked_days or 0 for tc in employee["timecards"] if tc.month == month]),
                    vacation_days_taken=sum([tc.paid_leave_days or 0 for tc in employee["timecards"] if tc.year == year]),
                    bonuses=sum([b.amount or 0.0 for b in employee["bonuses"]]) if employee["bonuses"] else 0.0
                ))
            return response
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve employees by manager email: {str(e)}")

    def _build_payroll_record_create(self, result, month, year):
        from decimal import Decimal
        def to_float(val):
            return float(val) if isinstance(val, Decimal) else val

        is_dict = isinstance(result, dict)
        def get_value(key, default=None):
            return result.get(key, default) if is_dict else getattr(result, key, default)

        return PayrollRecordCreate(
            employee_id=get_value('employee_id', None),
            payroll_year=year,
            payroll_month=month,
            employee_full_name=str(get_value('employee_full_name', '')),
            employee_national_id=str(get_value('employee_national_id', '')),
            employee_position=str(get_value('position', '')),
            employee_department=str(get_value('discipline', '')) if is_dict else str(get_value('department', '')),
            employee_base_salary=to_float(get_value('base_salary', 0.0)),
            employee_net_salary=0.0,
            employee_net_income=0.0,
            employee_base_before_taxes=0.0,
            employee_tax_percentage=to_float(get_value('tax_percent', 0.0)),
            employee_tax_amount=0.0,
            employee_health_percent=to_float(get_value('health_percent', 0.0)),
            employee_health_amount=0.0,
            employee_pension_amount=0.0,
            employee_pension_percent=to_float(get_value('pension_percent', 0.0)),
            employee_other_deductions=to_float(get_value('other_deduction_amounts', 0.0)),
            employee_worked_days=int(get_value('worked_days', 0)),
            employee_leave_days=int(get_value('leave_days', 0)),
            employee_meal_ticket_amount=to_float(get_value('meal_ticket_value', 0.0)),
            employee_other_benefits=to_float(get_value('other_bonuses', 0.0)),
            employee_bonus_amount=to_float(get_value('bonuses_sum', 0.0)),
        )

    async def get_employee_info_for_payroll(self, employee_email: str, month: int, year: int):
        try:
            logger = get_logger(__name__)
            logger.info(f"Fetching payroll info for {employee_email} - {month}/{year}")
            result = await self.employee_repository.get_employee_info_for_payroll(employee_email, month, year)
            logger.info(f"Payroll info retrieved: {result}")
            payroll_create = self._build_payroll_record_create(result, month, year)
            return payroll_create
        except ResourceNotFoundException as e:
            get_logger(__name__).warning(f"Payroll info not found for {employee_email} - {month}/{year}")
            raise e
        except DatabaseException as e:
            get_logger(__name__).error(f"Database error occurred while fetching payroll info for {employee_email} - {month}/{year}: {str(e)}")
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve employee info for payroll: {str(e)}")

