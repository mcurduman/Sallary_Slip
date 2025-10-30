from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, Date, Numeric
import uuid
from datetime import date
from app.db.base import Base

from typing import Optional

class EmployeeBaseSalary(Base):
    __tablename__ = "emp_base_salary"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("employee.id"), nullable=False)
    base_salary: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    tax_percentage: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    effective_start_date: Mapped[Optional[date]] = mapped_column(Date)
    effecitve_end_date: Mapped[Optional[date]] = mapped_column(Date)
    
    employee = relationship("Employee", back_populates="base_salary")
