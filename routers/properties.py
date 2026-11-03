from fastapi import APIRouter, HTTPException, status, Query, Response

from schemas.property import (PropertyCreate, PropertyUpdate, ResponseWithList, ResponseWithObject, ResponseWithoutData)

from data.store import properties

router = APIRouter()

@router.get("/get-properties", response_model=ResponseWithList)
def get_properties():
    return {
        "status": True,
        "message" : "Properties fetched successfully",
        "properties": properties
    }


@router.get("/get-property/{property_id}", response_model=ResponseWithObject)
def get_property(property_id: int):
    for item in properties:
        if item["id"] == property_id:
            return {
                "status": True,
                "message" : "Property fetched successfully",
                "property": item
            }

    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Property not found"
    )


@router.get("/search", response_model=ResponseWithList)
def search_properties(city: str = Query(min_length=2)):    
    properties_list = [item for item in properties if item["address"]["city"].lower() == city.lower()]

    return {
        "status": True,
        "message" : "Properties fetched successfully",
        "properties": properties_list
    }


@router.post(
    "/create-property", 
    response_model = ResponseWithObject, 
    status_code = status.HTTP_201_CREATED
)
def create_property(property_data: PropertyCreate):
    new_property = property_data.model_dump()
    new_property["id"] = len(properties) + 1
    properties.append(new_property)
    return {
        "status": True,
        "message" : "Property listed successfully",
        "property": new_property
    }


@router.put(
    "/update-property/{property_id}",
    response_model=ResponseWithObject
)
def update_property(property_id: int, property_data: PropertyCreate):
    for index, item in enumerate(properties):
        if item["id"] == property_id:
            updated_property = property_data.model_dump()
            updated_property["id"] = property_id
            properties[index] = updated_property

            return {
                "status": True,
                "message" : "Property updated successfully",
                "property": updated_property
            }

    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Property not found"
    )
    

@router.patch(
    "/patch-property/{property_id}",
    response_model=ResponseWithObject
)
def patch_property(property_id: int, property_data: PropertyUpdate):
    for item in properties:
        if item["id"] == property_id:
            update_data = property_data.model_dump(exclude_unset=True)
            item.update(update_data)

            return {
                "status": True,
                "message" : "Property updated successfully",
                "property": item
            }

    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Property not found"
    )    


@router.delete(
    "/delete-property/{property_id}",
    response_model=ResponseWithoutData,
    # status_code=status.HTTP_204_NO_CONTENT
)
def delete_property(property_id: int):
    for index, item in enumerate(properties):
        if item["id"] == property_id:
            properties.pop(index)

            response_content = {
                "status": True,
                "message" : "Property deleted successfully"
            }

            return Response(response_content, status_code = status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Property not found"
    )