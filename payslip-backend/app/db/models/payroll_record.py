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
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    gross_pay: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    net_pay: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    total_deductions: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    run_date: Mapped[Optional[date]] = mapped_column(Date)

    employee = relationship("Employee", back_populates="payroll_records")

    