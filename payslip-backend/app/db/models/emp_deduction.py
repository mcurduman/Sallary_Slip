from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Numeric, ForeignKey, Date, Enum
import uuid
from datetime import date
from typing import Optional
from app.db.base import Base
from app.utils.enums.periodicity_enum import Periodicity
from app.utils.enums.deduction_type_enum import DeductionType
from app.utils.enums.calculation_method_enum import CalculationMethod


class EmployeeDeduction(Base):
    __tablename__ = "emp_deduction"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("employee.id"), nullable=False)
    type: Mapped[DeductionType] = mapped_column(Enum(DeductionType), nullable=False)
    effective_start_date: Mapped[Optional[date]] = mapped_column(Date)
    effective_end_date: Mapped[Optional[date]] = mapped_column(Date)
    periodicity: Mapped[Periodicity] = mapped_column(Enum(Periodicity), nullable=False, default=Periodicity.MONTHLY)
    percentage: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    amount: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    calculation_method: Mapped[CalculationMethod] = mapped_column(
        Enum(CalculationMethod),
        nullable=False,
        default=CalculationMethod.FIXED
    )

    employee = relationship("Employee", back_populates="deductions")

    