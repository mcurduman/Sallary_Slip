from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String
import uuid
from app.db.base import Base

class Discipline(Base):
    __tablename__ = "discipline"
    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default = uuid.uuid4)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    employees = relationship("Employee", cascade="all, delele-orphan", back_populates="discipline")