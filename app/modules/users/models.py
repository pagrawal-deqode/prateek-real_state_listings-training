from sqlalchemy import String, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin
from app.common.enums import UserStatus

class User(TimestampMixin, Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    first_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    middle_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    last_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    status: Mapped[UserStatus] = mapped_column(
        SQLAlchemyEnum(
            UserStatus,
            name="user_status",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
            native_enum=True,
            validate_strings=True
        ),
        default=UserStatus.ACTIVE,
        server_default=UserStatus.ACTIVE,
        nullable=False
    )

    # Role assigned to this user.
    role: Mapped["Role"] = relationship(
        back_populates="users"
    )

    # Properties listed by this user.
    listed_properties: Mapped[list["Property"]] = relationship(
        back_populates="listed_by_user",
        foreign_keys="Property.listed_by"
    )

    # Favorites created by this user.
    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="user",
        passive_deletes=True
    )

    # Inquiries sent by this user.
    sent_inquiries: Mapped[list["Inquiry"]] = relationship(
        back_populates="sender",
        foreign_keys="Inquiry.sender_id"
    )

    # Reports submitted by this user.
    reported_listings: Mapped[list["ReportedListing"]] = relationship(
        back_populates="reporter",
        foreign_keys="ReportedListing.reporter_id"
    )

    reported_users: Mapped[list["ReportedUser"]] = relationship(
        back_populates="reporter",
        foreign_keys="ReportedUser.reporter_id"
    )

    reports_received: Mapped[list["ReportedUser"]] = relationship(
        back_populates="reported_user",
        foreign_keys="ReportedUser.user_id"
    )

    blocked_user_records: Mapped[list["BlockedUser"]] = relationship(
        back_populates="blocked_user",
        foreign_keys="BlockedUser.user_id"
    )