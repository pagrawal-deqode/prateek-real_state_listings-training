from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.common.enums import ListingStatus, ListingType, PropertyCategory


# --------------------------------
# Property Create Schema
# --------------------------------
class PropertyCreate(BaseModel):
    listed_by: int = Field(gt=0)
    title: str = Field(min_length=5, max_length=200)
    description: str | None = None

    property_category: PropertyCategory
    listing_type: ListingType

    sale_price: Decimal | None = Field(default=None, gt=0)
    rent_amount: Decimal | None = Field(default=None, gt=0)

    area_sqft: Decimal = Field(gt=0)

    bedrooms: int | None = Field(default=None, ge=0)
    bathrooms: int | None = Field(default=None, ge=0)

    address: str = Field(min_length=3)
    city: str = Field(min_length=2)
    state: str = Field(min_length=2)
    pincode: str = Field(min_length=6, max_length=6)

    @model_validator(mode="after")
    def validate_listing_price(self):

        if self.listing_type == ListingType.SALE:

            if self.sale_price is None:
                raise ValueError(
                    "Sale price is required for SALE listings"
                )

            if self.rent_amount is not None:
                raise ValueError(
                    "Rent amount must not be provided for SALE listings"
                )

        elif self.listing_type == ListingType.RENT:

            if self.rent_amount is None:
                raise ValueError(
                    "Rent amount is required for RENT listings"
                )

            if self.sale_price is not None:
                raise ValueError(
                    "Sale price must not be provided for RENT listings"
                )

        return self


# --------------------------------
# Property Update Schema
# --------------------------------
class PropertyUpdate(BaseModel):

    title: str | None = Field(default=None, min_length=5, max_length=200)
    description: str | None = None

    property_category: PropertyCategory | None = None
    listing_type: ListingType | None = None

    sale_price: Decimal | None = Field(default=None, gt=0)
    rent_amount: Decimal | None = Field(default=None, gt=0)

    area_sqft: Decimal | None = Field(default=None, gt=0)

    bedrooms: int | None = Field(default=None, ge=0)
    bathrooms: int | None = Field(default=None, ge=0)

    address: str | None = Field(default=None, min_length=3)
    city: str | None = Field(default=None, min_length=2)
    state: str | None = Field(default=None, min_length=2)
    pincode: str | None = Field(default=None, min_length=6, max_length=6)

    status: ListingStatus | None = None

# --------------------------------
# Property Response Schema
# --------------------------------
class PropertyOut(BaseModel):
    id: int
    listed_by: int
    title: str
    description: str | None

    property_category: PropertyCategory
    listing_type: ListingType

    sale_price: Decimal | None
    rent_amount: Decimal | None

    area_sqft: Decimal

    bedrooms: int | None
    bathrooms: int | None

    address: str
    city: str
    state: str
    pincode: str

    status: ListingStatus

    model_config = ConfigDict(from_attributes=True)