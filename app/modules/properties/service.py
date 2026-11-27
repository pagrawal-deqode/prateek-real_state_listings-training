from fastapi import HTTPException, status
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from app.common.enums import ListingStatus
from app.modules.properties import repository
from app.modules.properties.schemas import PropertyCreate

def create_property(db:Session, property_data: PropertyCreate):
    data = property_data.model_dump()
    data["status"] = ListingStatus.PENDING

    try:
        return repository.create_property(db, data)
    
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Invalid property data or listed_by user does not exist"
        )

def get_all_properties(db: Session, skip: int = 0, limit: int = 10):
    return repository.get_all_properties(db=db, skip=skip, limit=limit)

def get_property_by_id(db: Session, property_id: int):
    property_obj = repository.get_property_by_id(db=db, property_id=property_id)

    if property_obj is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Property not found"
        )

    return property_obj

def update_property(db: Session, property_id: int, update_data: dict):
    property_obj = get_property_by_id(db=db, property_id=property_id)

    # Keep only the fields the client actually provided.
    changes = { key: value for key, value in update_data.items()}

    # Build the complete current property state.
    current_data = {
        "listed_by": property_obj.listed_by,
        "title": property_obj.title,
        "description": property_obj.description,
        "property_category": property_obj.property_category,
        "listing_type": property_obj.listing_type,
        "sale_price": property_obj.sale_price,
        "rent_amount": property_obj.rent_amount,
        "area_sqft": property_obj.area_sqft,
        "bedrooms": property_obj.bedrooms,
        "bathrooms": property_obj.bathrooms,
        "address": property_obj.address,
        "city": property_obj.city,
        "state": property_obj.state,
        "pincode": property_obj.pincode
    }

    # Merge existing values with the new values.
    current_data.update(changes)

    # Validate the final property state, including
    # the SALE/RENT price rules.
    try:
        validated_data = PropertyCreate.model_validate(current_data)

    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.errors()
        )

    try:
        return repository.update_property(
            db=db,
            property_obj=property_obj,
            update_data=changes
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Property update violates a database constraint"
        )

def delete_property(db:Session, property_id: int):
    property_obj = get_property_by_id(db=db, property_id=property_id)

    try:
        repository.delete_property(db=db, property_obj=property_obj)
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Property can not be deleted becuase related records exist"
        )

