from decimal import Decimal
from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    Numeric,
    Integer,
    CheckConstraint,
    Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin
from app.common.enums import ListingStatus, ListingType, PropertyCategory

class Property(TimestampMixin, Base):
    __tablename__ = "properties"

    __table_args__ = (
        CheckConstraint(
            "bedrooms >= 0",
            name="ck_properties_bedrooms"
        ),
        CheckConstraint(
            "bathrooms >= 0",
            name="ck_properties_bathrooms"
        ),
        CheckConstraint(
            "area_sqft > 0",
            name="ck_properties_area_sqft"
        ),
        CheckConstraint(
            """
            (
                listing_type = 'SALE'
                AND sale_price IS NOT NULL
                AND sale_price > 0
                AND rent_amount IS NULL
            )
            OR
            (
                listing_type = 'RENT'
                AND rent_amount IS NOT NULL
                AND rent_amount > 0
                AND sale_price IS NULL
            )
            """,
            name="ck_properties_listing_amount"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    listed_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    property_category: Mapped[PropertyCategory] = mapped_column(
        SQLAlchemyEnum(
            PropertyCategory,
            name="property_category",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
            native_enum=True,
            validate_strings=True
        ),
        nullable=False
    )

    listing_type: Mapped[ListingType] = mapped_column(
        SQLAlchemyEnum(
            ListingType,
            name="listing_type",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
            native_enum=True,
            validate_strings=True
        ),
        nullable=False
    )

    sale_price: Mapped[Decimal | None] = mapped_column(
        Numeric(14, 2),
        nullable=True
    )

    rent_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True
    )

    area_sqft: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    bedrooms: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    bathrooms: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0"
    )

    address: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    pincode: Mapped[str] = mapped_column(
        String(6),
        nullable=False
    )

    status: Mapped[ListingStatus] = mapped_column(
        SQLAlchemyEnum(
            ListingStatus,
            name="listing_status",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
            native_enum=True,
            validate_strings=True
        ),
        default=ListingStatus.PENDING,
        server_default=ListingStatus.PENDING.value,
        nullable=False
    )

    # User who listed this property.
    listed_by_user: Mapped["User"] = relationship(
        back_populates="listed_properties",
        foreign_keys=[listed_by]
    ) 

    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="property",
        passive_deletes=True
    )

    inquiries: Mapped[list["Inquiry"]] = relationship(
        back_populates="property"
    )

    reported_records: Mapped[list["ReportedListing"]] = relationship(
        back_populates="property"
    )

    blocked_records: Mapped[list["BlockedListing"]] = relationship(
        back_populates="property"
    )   
