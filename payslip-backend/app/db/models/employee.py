from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Integer, String, Boolean, ForeignKey, Date, Text, Numeric
import uuid
from datetime import date
from app.db.base import Base
from typing import Optional

class Employee(Base):
    __tablename__ = "employee"
    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default = uuid.uuid4)
    national_id:  Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    middle_name:  Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    position_id: Mapped[uuid.uuid4] = mapped_column(ForeignKey("position.id"), nullable=False)
    manager_id: Mapped[uuid.uuid4] = mapped_column(ForeignKey("employee.sk"), nullable=False)
    discipline_id: Mapped[uuid.uuid4] = mapped_column(ForeignKey("discipline.id"), nullable=False)

    position = relationship("Position", back_populates="positions")
    discipline = relationship("Discipline", back_populates="positions")
    manager = relationship("Employee",remote_side=[id])
    deductions = relationship("EmployeeDeductions", cascade="all, delete-orphan", back_populates="employee")
    base_salary = relationship("EmployeeBaseSalary", cascade="all, delete-orphan", back_populates="employee")
    benefits = relationship("EmployeeBenefits", cascade="all, delete-orphan", back_populates="employee")
    pay_roll_records = relationship("PayRollRecord", cascade="all, delete-orphan", back_populates="employee")

