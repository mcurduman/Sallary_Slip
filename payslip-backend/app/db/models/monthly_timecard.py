from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Numeric, ForeignKey
import uuid
from app.db.base import Base

class Timecard(Base):
    __tablename__ = "timecard"
    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default = uuid.uuid4)
    month: 
    approved_by:
    worked_days:
    paid_days_of:
    unpaid_days_of:
    worked_hours:
    overtime_hours:
    



    

    position = relationship("Position", back_populates="deductions")

    