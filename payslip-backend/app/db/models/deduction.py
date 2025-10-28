from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Numeric, ForeignKey
import uuid
from app.db.base import Base

class Deduction(Base):
    __tablename__ = "deduction"
    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default = uuid.uuid4)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    position_id: Mapped[uuid.uuid4] = mapped_column(ForeignKey("position.id"), nullable=False)
    percentage: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    position = relationship("Position", back_populates="deductions")

    