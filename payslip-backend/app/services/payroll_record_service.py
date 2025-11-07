from app.schemas.payroll_record.payroll_record_create import PayrollRecordCreate
from app.db.models.payroll_record import PayrollRecord
from app.repositories.payroll_record_repository import PayrollRecordRepository
from typing import Optional, Iterable, List
import uuid
from app.schemas.payroll_record.payroll_record_response import PayrollRecordResponse
from app.utils.errors.DatabaseException import DatabaseException
from app.utils.errors.ResourceNotFoundException import ResourceNotFoundException
from app.utils.errors.BaseAppException import BaseAppException
from app.core.logging import get_logger
from datetime import date

class PayrollRecordService:
    def __init__(self, payroll_record_repository: PayrollRecordRepository):
        self.payroll_record_repository = payroll_record_repository

    def _calculate_salary_components(self, payroll_record: PayrollRecordCreate) -> None:
        get_logger().info(f"Calculating salary components for payroll record: {payroll_record}")
        payroll_record.employee_health_amount = (
            payroll_record.employee_base_salary * payroll_record.employee_health_percent / 100
        )
        get_logger().info(f"Health amount calculated: {payroll_record.employee_health_amount}")
        payroll_record.employee_pension_amount = (
            payroll_record.employee_base_salary * payroll_record.employee_pension_percent / 100
        )
        get_logger().info(f"Pension amount calculated: {payroll_record.employee_pension_amount}")
        payroll_record.employee_net_income = (
            payroll_record.employee_base_salary
            - payroll_record.employee_health_amount
            - payroll_record.employee_pension_amount
            - payroll_record.employee_other_deductions
        )
        get_logger().info(f"Net income calculated: {payroll_record.employee_net_income}")
        payroll_record.employee_base_before_taxes = (
            payroll_record.employee_net_income
            + payroll_record.employee_bonus_amount
            + payroll_record.employee_other_benefits
            + (payroll_record.employee_meal_ticket_amount if payroll_record.employee_meal_ticket_amount else 0) * payroll_record.employee_worked_days
        )
        get_logger().info(f"Before taxes calculated: {payroll_record.employee_base_before_taxes}")
        payroll_record.employee_tax_amount = (
            payroll_record.employee_base_before_taxes * payroll_record.employee_tax_percentage / 100
        )
        get_logger().info(f"Tax amount calculated: {payroll_record.employee_tax_amount}")
        payroll_record.employee_net_salary = (
            payroll_record.employee_net_income - payroll_record.employee_tax_amount
        )
        get_logger().info(f"Calculated payroll record: {payroll_record}")



    async def generate_payroll_report(self, payroll_record: PayrollRecordCreate):
        try:
            get_logger().info(f"Creating payroll record for employee ID: {payroll_record.employee_id}")
            self._calculate_salary_components(payroll_record)
            payroll_record_model = PayrollRecord(**payroll_record.model_dump())
            payroll_record_model.run_date = date.today()
            get_logger().info(f"Created payroll record: {payroll_record_model}")
            await self.payroll_record_repository.create(payroll_record_model)
            get_logger().info(f"Payroll record saved to repository: {payroll_record_model}")
            return payroll_record_model
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to create payroll record: {str(e)}")
        
    async def get_payroll_record_by_id(self, payroll_record_id: uuid.UUID
        ) -> Optional[PayrollRecord]:
        try:
            return await self.payroll_record_repository.get(payroll_record_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve payroll record: {str(e)}")

    async def get_payroll_data(self, employee_id: uuid.UUID, month: int, year: int) -> Iterable[PayrollRecord]:
        try:
            return await self.payroll_record_repository.get_payroll_data(employee_id, month, year)
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve payroll data: {str(e)}")
        
    async def get_all_payroll_records(self) -> Iterable[PayrollRecord]:
        try:
            return await self.payroll_record_repository.get_all()
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve payroll records: {str(e)}")

    async def get_all_by_ids(self, ids_list: List[uuid.UUID], month: int, year: int) -> Iterable[PayrollRecord]:
        try:
            return await self.payroll_record_repository.get_all_by_ids(ids_list, month, year)
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve payroll records for manager: {str(e)}")
        
    def from_model_to_response(self, payroll_record: PayrollRecord) -> PayrollRecordResponse:
        try:
            response = PayrollRecordResponse(
                run_date=payroll_record.run_date.strftime("%Y-%m-%d") if payroll_record.run_date else None,
                payroll_month=payroll_record.payroll_month,
                payroll_year=payroll_record.payroll_year
            )
            return response
        except Exception as e:
            raise BaseAppException(f"Failed to convert payroll record to response model: {str(e)}") 

    async def get_by_employee_email(self, employee_email: str) -> Iterable[PayrollRecordResponse]:
        try:
            result = await self.payroll_record_repository.get_by_employee_email(employee_email)
            return [self.from_model_to_response(record) for record in result]
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve payroll records: {str(e)}")