from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, ForeignKey, Date
import uuid
from datetime import date
from app.db.base import Base
from typing import Optional
from app.utils.enums.employment_status_enum import EmploymentStatus

class Employee(Base):
    __tablename__ = "employee"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    national_id: Mapped[str] = mapped_column(String, nullable=False)
    country_of_id: Mapped[Optional[str]] = mapped_column(String)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    position_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("position.id"), nullable=False)
    manager_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("employee.id"))
    discipline_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("discipline.id"))
    employment_status: Mapped[EmploymentStatus] = mapped_column(String, default=EmploymentStatus.ACTIVE)
    hire_date: Mapped[Optional[date]] = mapped_column(Date)
    termination_status: Mapped[Optional[EmploymentStatus]] = mapped_column(String, default=None)
    termination_date: Mapped[Optional[date]] = mapped_column(Date)

    user = relationship("User", back_populates="employee")
    position = relationship("Position", back_populates="employees")
    discipline = relationship("Discipline", back_populates="employees")
    manager = relationship("Employee", remote_side=[id], back_populates="direct_reports")
    direct_reports = relationship("Employee", back_populates="manager")
    monthly_timecards = relationship("MonthlyTimecard", back_populates="employee")
    approved_monthly_timecards = relationship("MonthlyTimecard", back_populates="approver", foreign_keys='MonthlyTimecard.approved_by')
    payroll_records = relationship("PayrollRecord", back_populates="employee")
    deductions = relationship("Deduction", back_populates="employee")
    base_salary = relationship("EmployeeBaseSalary", back_populates="employee")
    benefits = relationship("EmployeeBenefit", back_populates="employee")

