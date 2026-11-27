from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.properties import service
from app.modules.properties.schemas import (PropertyCreate, PropertyUpdate, PropertyOut)

router = APIRouter(
    prefix="/properties",
    tags=["Properties"]
)

@router.post(
    "/create-property",
    response_model=PropertyOut,
    status_code=status.HTTP_201_CREATED
)
def create_property(property_data: PropertyCreate, db:Session = Depends(get_db)):
    return service.create_property(db=db, property_data=property_data)

@router.get(
    "/get-all-properties",
    response_model=list[PropertyOut],
    status_code=status.HTTP_200_OK
)
def get_all_properties(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return service.get_all_properties(db=db, skip=skip, limit=limit)

@router.get(
    "get-property/{property_id}",
    response_model=PropertyOut,
    status_code=status.HTTP_200_OK
)
def get_property_by_id(property_id: int, db: Session = Depends(get_db)):
    return service.get_property_by_id(db=db, property_id=property_id)

@router.patch(
    "/update-property/{property_id}",
    response_model=PropertyOut,
    status_code=status.HTTP_200_OK
)
def update_property(
    property_id: int, 
    property_data: PropertyUpdate, 
    db: Session = Depends(get_db)
):
    update_data = property_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="At least one field must be provided for update"
        )

    service.update_property(db=db, property_id=property_id, update_data=update_data)


@router.delete(
    "delete-property/{property_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_property(property_id: int, db: Session = Depends(get_db)):
    service.delete_property(db=db, property_id=property_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)