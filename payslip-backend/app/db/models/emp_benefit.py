from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, Date, Numeric, Boolean, Enum
import uuid
from datetime import date
from typing import Optional

from app.utils.enums.calculation_method_enum import CalculationMethod
from app.utils.enums.periodicity_enum import Periodicity
from app.utils.enums.benefit_type_enum import BenefitType


class EmployeeBenefit:
    __tablename__ = "emp_benefit"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("employee.id"), nullable=False)
    type: Mapped[BenefitType] = mapped_column(Enum(BenefitType), nullable=False)
    amount: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    percentage: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    calculation_method: Mapped[CalculationMethod] = mapped_column(
        Enum(CalculationMethod),
        nullable=False,
        default=CalculationMethod.fixed
    )

    taxable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    periodicity: Mapped[Periodicity] = mapped_column(
        Enum(Periodicity),
        nullable=False,
        default=Periodicity.monthly
    )
    effective_start_date: Mapped[Optional[date]] = mapped_column(Date)
    effective_end_date: Mapped[Optional[date]] = mapped_column(Date)

    employee = relationship("Employee", back_populates="benefits")