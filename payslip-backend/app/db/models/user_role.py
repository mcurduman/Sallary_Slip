from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum, ForeignKey
import uuid
from app.db.base import Base
from app.utils.enums.user_role_enum import UserRole

class UserRoleModel(Base):
    __tablename__ = "user_roles"
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, primary_key=True)
