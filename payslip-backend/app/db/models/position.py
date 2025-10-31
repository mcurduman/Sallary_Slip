from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String
import uuid
from app.db.base import Base

class Position(Base):
    __tablename__ = "position"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default = uuid.uuid4)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    employees = relationship("Employee", cascade="all, delete-orphan", back_populates="position")