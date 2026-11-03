from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class Address(BaseModel):
    house_number: str = Field(min_length=1)
    street: str = Field(min_length=2)
    city: str = Field(min_lenght=2)
    state: str = Field(min_lenght=2)
    pincode: str = Field(min_length=6, max_length=6)

class PropertyCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=5, max_length=100)
    description: str | None = None
    price: float = Field(gt=0)
    property_type: Literal["Apartment", "House", "Villa", "Plot"]
    listing_type: Literal["Sale", "Rent"]
    bedrooms: int = Field(ge=0)
    bathrooms: int = Field(ge=0)
    area_sqft: float = Field(gt=0)
    is_available: bool = True
    address: Address

class PropertyUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=5, max_length=100)
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    property_type: Literal["Apartment", "House", "Villa", "Plot"] | None = None
    listing_type: Literal["Sale", "Rent"] | None = None
    bedrooms: int | None = Field(default=None, ge=0)
    bathrooms: int | None = Field(default=None, ge=0)
    area_sqft: float | None = Field(default=None, gt=0)
    is_available: bool | None = None
    address: Address | None = None

class PropertyResponse(PropertyCreate):
    id: int

class ResponseWithoutData(BaseModel):
    status: bool
    message: str

class ResponseWithList(ResponseWithoutData):
    properties: list[PropertyResponse]

class ResponseWithObject(ResponseWithoutData):
    property: PropertyResponse
