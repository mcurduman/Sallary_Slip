from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer, ForeignKey, Numeric, Date
import uuid
from typing import Optional
from app.db.base import Base
from datetime import date

class PayrollRecord(Base):
    __tablename__ = "payroll_record"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("employee.id"), nullable=False)
    payroll_year: Mapped[int] = mapped_column(Integer, nullable=False)
    payroll_month: Mapped[int] = mapped_column(Integer, nullable=False)

    employee_full_name: Mapped[str] = mapped_column(String(128))
    employee_national_id: Mapped[str] = mapped_column(String(32))
    employee_position: Mapped[str] = mapped_column(String(64))
    employee_department: Mapped[str] = mapped_column(String(64))

    employee_base_salary: Mapped[float] = mapped_column(Numeric(12, 2))
    employee_net_salary: Mapped[float] = mapped_column(Numeric(12, 2))
    employee_net_income: Mapped[float] = mapped_column(Numeric(12, 2))
    employee_base_before_taxes: Mapped[float] = mapped_column(Numeric(12, 2))

    employee_tax_percentage: Mapped[float] = mapped_column(Numeric(5, 2))
    employee_tax_amount: Mapped[float] = mapped_column(Numeric(12, 2))
    employee_health_percent: Mapped[float] = mapped_column(Numeric(5, 2))
    employee_health_amount: Mapped[float] = mapped_column(Numeric(12, 2))
    employee_pension_amount: Mapped[float] = mapped_column(Numeric(12, 2))
    employee_pension_percent: Mapped[float] = mapped_column(Numeric(5, 2))
    employee_other_deductions: Mapped[float] = mapped_column(Numeric(12, 2))

    employee_worked_days: Mapped[int] = mapped_column(Integer)
    employee_leave_days: Mapped[int] = mapped_column(Integer)

    employee_meal_ticket_amount: Mapped[float] = mapped_column(Numeric(12, 2))
    employee_other_benefits: Mapped[float] = mapped_column(Numeric(12, 2))
    employee_bonus_amount: Mapped[float] = mapped_column(Numeric(12, 2))
    run_date: Mapped[Optional[date]] = mapped_column(Date)

    employee = relationship("Employee", back_populates="payroll_records")

    