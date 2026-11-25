from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin


# ---------------------------------------------------------
# 1. Reported Listing
# ---------------------------------------------------------

class ReportedListing(TimestampMixin, Base):

    __tablename__ = "reported_listings"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    property_id: Mapped[int] = mapped_column(
        ForeignKey("properties.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    reporter_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    property: Mapped["Property"] = relationship(
        back_populates="reported_records"
    )

    reporter: Mapped["User"] = relationship(
        back_populates="reported_listings",
        foreign_keys=[reporter_id]
    )


# ---------------------------------------------------------
# 2. Blocked Listing
# ---------------------------------------------------------

class BlockedListing(TimestampMixin, Base):

    __tablename__ = "blocked_listings"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    property_id: Mapped[int] = mapped_column(
        ForeignKey("properties.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    property: Mapped["Property"] = relationship(
        back_populates="blocked_records"
    )


# ---------------------------------------------------------
# 3. Reported User
# ---------------------------------------------------------

class ReportedUser(TimestampMixin, Base):

    __tablename__ = "reported_users"

    __table_args__ = (
        CheckConstraint(
            "user_id <> reporter_id",
            name="ck_reported_users_no_self_report"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    # User being reported.
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    # User submitting the report.
    reporter_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    reported_user: Mapped["User"] = relationship(
        back_populates="reports_received",
        foreign_keys=[user_id]
    )

    reporter: Mapped["User"] = relationship(
        back_populates="reported_users",
        foreign_keys=[reporter_id]
    )


# ---------------------------------------------------------
# 4. Blocked User
# ---------------------------------------------------------

class BlockedUser(TimestampMixin, Base):

    __tablename__ = "blocked_users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    # User who is being blocked.
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    blocked_user: Mapped["User"] = relationship(
        back_populates="blocks_received",
        foreign_keys=[user_id]
    )