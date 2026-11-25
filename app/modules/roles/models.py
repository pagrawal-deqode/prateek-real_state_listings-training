from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin

class Role(TimestampMixin, Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(50), 
        unique=True, 
        nullable=False
    )
    
    description: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )

    # One role can belong to multiple users.
    users: Mapped[list["User"]] = relationship(
        back_populates="role"
    )