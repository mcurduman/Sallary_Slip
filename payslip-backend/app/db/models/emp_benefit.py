from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, Date, Numeric, String
import uuid
from datetime import date
from app.db.base import Base

class EmployeeBenefit(Base):
    __tablename__ = "emp_benefit"
    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default = uuid.uuid4)
    employee_id: Mapped[uuid.uuid4] = mapped_column(ForeignKey("employee.sk"), nullable=False)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    fixed_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)

    employee = relationship("Employee", back_populates="emp_benefit")