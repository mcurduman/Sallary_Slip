from typing import Optional, Iterable
from app.utils.enums.benefit_type_enum import BenefitType
from app.utils.enums.deduction_type_enum import DeductionType
from app.schemas.employee.employee_details import EmployeeDetails
from app.db.models.employee import Employee
from app.repositories.base_repository import BaseRepository
from app.utils.errors.DatabaseException import DatabaseException
from app.utils.errors.ResourceNotFoundException import ResourceNotFoundException
import uuid
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.core.logging import get_logger

logger = get_logger(__name__)

class EmployeeRepository(BaseRepository[Employee, uuid.UUID]):
    _emp_not_found_msg = "Employee not found"

    async def get(self, id: uuid.UUID) -> Optional[Employee]:
        try:
            employee = await self._session.execute(select(Employee).where(Employee  .id == id))
            if not employee:
                raise ResourceNotFoundException(self._emp_not_found_msg)
            return employee.first()
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve employee: {str(e)}")

    async def get_by_email(self, email: str) -> Optional[Employee]:
        try:
            result = await self._session.execute(select(Employee).where(Employee.email == email))
            employee = result.scalars().first()
            if not employee:
                raise ResourceNotFoundException(self._emp_not_found_msg)
            return employee
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve employee: {str(e)}")

    async def get_managers(self) -> Iterable[Employee]:
        try:
            result = await self._session.execute(
                select(Employee).where(Employee.id.in_(
                    select(Employee.manager_id).distinct().where(Employee.manager_id.isnot(None))
                ))
            )
            managers = result.unique().scalars().all()
            return managers
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve managers: {str(e)}")
        
    async def get_employee_all_details(self, employee_id: uuid.UUID) -> Optional[Employee]:
        try:
            result = await self._session.execute(
            select(Employee)
            .where(Employee.id == employee_id)
            .options(
                joinedload(Employee.position),
                joinedload(Employee.discipline)
            )
            )
            employee = result.scalars().first()
            if not employee:
                raise ResourceNotFoundException(self._emp_not_found_msg)
            return employee
        except Exception as e:
                raise DatabaseException(f"Failed to retrieve employee details: {str(e)}")
    
    async def is_manager(self, employee_id: uuid.UUID) -> bool:
        try:
            result = await self._session.execute(
                select(Employee).where(Employee.manager_id == employee_id)
            )
            employees = result.unique().scalars().all()
            return len(employees) > 0
        except Exception as e:
            raise DatabaseException(f"Failed to check if employee is a manager: {str(e)}")

    async def create(self, entity: Employee) -> Employee:
        try:
            self._session.add(entity)
            await self._session.flush()
            return entity
        except Exception as e:
            raise DatabaseException(f"Failed to create employee: {str(e)}")

    async def get_all(self) -> Iterable[Employee]:
        try:
            result = await self._session.execute(
                select(Employee)
                .options(
                    joinedload(Employee.position),
                    joinedload(Employee.discipline)
                )
            )
            employees = result.unique().scalars().all()
            return employees
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve employees: {str(e)}")

    async def delete(self, id: uuid.UUID) -> None:
        try:
            employee = await self.get(id)
            if not employee:
                raise ResourceNotFoundException(self._emp_not_found_msg)
            await self._session.delete(employee)
        except Exception as e:
            raise DatabaseException(f"Failed to delete employee: {str(e)}")

    async def update(self, entity: Employee) -> Employee:
        try:
            await self._session.merge(entity)
            await self._session.flush()
            return entity
        except Exception as e:
            raise DatabaseException(f"Failed to update position: {str(e)}")
        
    async def get_by_manager_email(self, manager_email: str, month: int, year: int):
        try:
            result = await self._session.execute(
                select(Employee)
                .where(Employee.manager.has(email=manager_email))
                .options(
                    joinedload(Employee.payroll_records),
                    joinedload(Employee.emp_benefits),
                    joinedload(Employee.monthly_timecards)
                )
            )
            employees = result.unique().scalars().all()
            data = []
            for emp in employees:
                payrolls = [pr for pr in emp.payroll_records if pr.payroll_month == month and pr.payroll_year == year]
                monthly_timecards = [tc for tc in emp.monthly_timecards if tc.year == year]
                bonuses = [b for b in emp.emp_benefits if b.type.name == "BONUS" and
                    (b.effective_start_date is None or (b.effective_start_date.month == month and b.effective_start_date.year == year))]
                data.append({
                    "employee": emp,
                    "timecards": monthly_timecards,
                    "payroll_records": payrolls,
                    "bonuses": bonuses
                })
            return data
        except Exception as e:
                raise DatabaseException(f"Failed to retrieve employees/payroll/bonuses: {str(e)}")
        
    def _map_to_employee_details(self, emp: Employee) -> EmployeeDetails:
        full_name = f"{emp.first_name} {emp.last_name}" if emp.middle_name is None else f"{emp.first_name} {emp.middle_name} {emp.last_name}"
        discipline = emp.discipline.name if emp.discipline else None
        position = emp.position.title if emp.position else None
        return EmployeeDetails(
            email=emp.email,
            full_name=full_name,
            discipline=discipline,
            position=position
        )

    async def get_employee_details_by_email(self, email: str) -> EmployeeDetails:
        try:
            result = await self._session.execute(
                select(Employee)
                .where(Employee.email == email)
                .options(
                    joinedload(Employee.position),
                    joinedload(Employee.discipline)
                )
            )
            employee = result.scalars().first()
            if not employee:
                raise ResourceNotFoundException("Employee not found")
            return self._map_to_employee_details(employee)
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve employee details: {str(e)}")

    async def get_employees_ids_and_mails_by_manager_email(self, manager_email: str) -> Iterable[uuid.UUID]:
        try:
            result = await self._session.execute(
                select(Employee)
                .where(Employee.manager.has(email=manager_email))
            )
            employees = result.scalars().all()
            return [(emp.id, emp.email) for emp in employees]
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve employee IDs by manager email: {str(e)}")

    async def get_employees_details_by_manager_email(self, manager_email: str) -> Iterable[EmployeeDetails]:
        try:
            result = await self._session.execute(
                select(Employee)
                .where(Employee.manager.has(email=manager_email))
                .options(
                    joinedload(Employee.position),
                    joinedload(Employee.discipline)
                )
            )
            employees = result.scalars().all()
            return [self._map_to_employee_details(emp) for emp in employees]
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve employee details by manager email: {str(e)}")

    def _get_benefits_info(self, benefits):
        bonuses_sum = sum([b.amount for b in benefits if hasattr(b, 'type') and b.type == BenefitType.BONUS])
        meal_ticket_value = sum([b.amount for b in benefits if hasattr(b, 'type') and b.type == BenefitType.MEAL])
        other_bonuses = sum([b.amount for b in benefits if hasattr(b, 'type') and b.type not in [BenefitType.BONUS, BenefitType.MEAL]])
        return bonuses_sum, meal_ticket_value, other_bonuses
    
    def _get_deductions_info(self, deductions):
        pension_percent = sum([d.percentage for d in deductions if hasattr(d, 'type') and d.type == DeductionType.PENSION])
        health_percent = sum([d.percentage for d in deductions if hasattr(d, 'type') and d.type == DeductionType.HEALTH])
        other_deduction_amounts = sum([getattr(d, 'amount', 0) for d in deductions if hasattr(d, 'type') and d.type not in [DeductionType.PENSION, DeductionType.HEALTH]])
        return pension_percent, health_percent, other_deduction_amounts

    def _get_days_info(self, timecards, month, year):
        worked_days = sum([tc.worked_days or 0 for tc in timecards if tc.month == month and tc.year == year])
        leave_days = sum([tc.paid_leave_days or 0 for tc in timecards if tc.month == month and tc.year == year])
        return worked_days, leave_days
    
    def _filter_benefits(self, benefits, month, year):
        filtered = []
        for b in benefits:
            if b.effective_start_date is None:
                include = True
            else:
                include = (b.effective_start_date.year < year) or \
                          (b.effective_start_date.year == year and b.effective_start_date.month <= month)
            if include:
                filtered.append(b)
        return filtered

    def _filter_deductions(self, deductions, month, year):
        filtered = []
        for d in deductions:
            if d.effective_start_date is None:
                include = True
            else:
                include = (d.effective_start_date.year < year) or \
                          (d.effective_start_date.year == year and d.effective_start_date.month <= month)
            if d.effective_end_date is not None:
                include = include and ((d.effective_end_date.year > year) or \
                                       (d.effective_end_date.year == year and d.effective_end_date.month >= month))
            if include:
                filtered.append(d)
        return filtered

    async def get_employee_info_for_payroll(self, employee_email: str, month: int, year: int):
        try:
            result = await self._session.execute(
                select(Employee)
                .where(Employee.email == employee_email)
                .options(
                    joinedload(Employee.emp_benefits),
                    joinedload(Employee.monthly_timecards),
                    joinedload(Employee.deductions),
                    joinedload(Employee.base_salary),
                    joinedload(Employee.discipline),
                    joinedload(Employee.position)
                )
            )
            emp = result.scalars().first()
            if not emp:
                raise ResourceNotFoundException(self._emp_not_found_msg)
            monthly_timecards = [tc for tc in emp.monthly_timecards if tc.year == year]
            worked_days, leave_days = self._get_days_info(monthly_timecards, month, year)
            benefits = self._filter_benefits(emp.emp_benefits, month, year)
            bonuses_sum, meal_ticket_value, other_bonuses = self._get_benefits_info(benefits)
            deductions = self._filter_deductions(emp.deductions, month, year)
            pension_percent, health_percent, other_deduction_amounts = self._get_deductions_info(deductions)
            base_salary = emp.base_salary[0].base_salary if emp.base_salary else 0.0
            tax_percent = emp.base_salary[0].tax_percentage if emp.base_salary and emp.base_salary[0].tax_percentage else 0.0
            discipline = emp.discipline.name if emp.discipline else None
            position = emp.position.title if emp.position else None
            employee_id = emp.id
            employee_full_name = f"{emp.first_name} {emp.last_name}" if emp.middle_name is None else f"{emp.first_name} {emp.middle_name} {emp.last_name}"
            employee_national_id = emp.national_id
            data = {
                "employee_id": employee_id,
                "employee_full_name": employee_full_name,
                "employee_national_id": employee_national_id,
                "discipline": discipline,
                "position": position,
                "bonuses_sum": bonuses_sum,
                "meal_ticket_value": meal_ticket_value,
                "other_bonuses": other_bonuses,
                "pension_percent": pension_percent,
                "health_percent": health_percent,
                "other_deduction_amounts": other_deduction_amounts,
                "base_salary": base_salary,
                "tax_percent": tax_percent,
                "worked_days": worked_days,
                "leave_days": leave_days
            }
            return data
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve employee info for payroll: {str(e)}")