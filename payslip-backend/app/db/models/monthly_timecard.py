from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Integer, ForeignKey, String
import uuid
from typing import Optional
from app.utils.enums.timecard_status_enum import TimecardStatus
from app.db.base import Base

class MonthlyTimecard(Base):
    __tablename__ = "monthly_timecard"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("employee.id"), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    approved_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("employee.id"))
    worked_days: Mapped[Optional[int]] = mapped_column(Integer)
    paid_leave_days: Mapped[Optional[int]] = mapped_column(Integer)
    unpaid_leave_days: Mapped[Optional[int]] = mapped_column(Integer)
    worked_hours: Mapped[Optional[int]] = mapped_column(Integer)
    overtime_hours: Mapped[Optional[int]] = mapped_column(Integer)
    status : Mapped[Optional[TimecardStatus]] = mapped_column(String, default=TimecardStatus.DRAFT)

    employee = relationship("Employee", back_populates="monthly_timecards", foreign_keys=[employee_id])
    approver = relationship("Employee", foreign_keys=[approved_by], back_populates="approved_monthly_timecards")
