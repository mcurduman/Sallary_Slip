from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Enum, ForeignKey, Table, Column
import uuid
from app.db.base import Base
from app.utils.enums.user_role_enum import UserRole
from app.db.models.user_role import UserRoleModel
from typing import List

# UserRole table for many-to-many relationship
class User(Base):
    __tablename__ = "user"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(ForeignKey("employee.email"), unique=True, nullable=False)

    roles: Mapped[List[UserRoleModel]] = relationship(
        "UserRoleModel",
        backref="user",
        cascade="all, delete-orphan",
        lazy="joined"
    )

    employee = relationship("Employee", back_populates="user")