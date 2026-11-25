from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    DateTime,
    Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin
from app.common.enums import InquiryStatus

class Inquiry(TimestampMixin, Base):
    __tablename__ = "inquiries"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    property_id: Mapped[int] = mapped_column(
        ForeignKey("properties.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    sender_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    status: Mapped[InquiryStatus] = mapped_column(
        SQLAlchemyEnum(
            InquiryStatus,
            name="inquiry_status",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
            native_enum=True,
            validate_strings=True
        ),
        default=InquiryStatus.NEW,
        server_default=InquiryStatus.NEW.value,
        nullable=False
    )

    visit_scheduled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    property: Mapped["Property"] = relationship(
        back_populates="inquiries"
    )

    sender: Mapped["User"] = relationship(
        back_populates="sent_inquiries",
        foreign_keys=[sender_id]
    )
