from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String
import uuid
from app.db.base import Base

class Position(Base):
    __tablename__ = "position"
    id: Mapped[uuid.uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default = uuid.uuid4)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    grade: Mapped[str] = mapped_column(String, unique=True, nullable=False)