from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, ForeignKey, Numeric, Date
import uuid
from datetime import date
from app.db.base import Base

class Benefit(Base):
    __tablename__ = "benefit"
    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default = uuid.uuid4)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    position_id: Mapped[uuid.uuid4] = mapped_column(ForeignKey("position.id"), nullable=False)
    fixed_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    effective_date: Mapped[date] = mapped_column(Date, nullable=False)

    position = relationship("Position", back_populates="benefits")

    