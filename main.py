from fastapi import FastAPI, HTTPException, status, Query
from schemas.property import (PropertyCreate, PropertyResponse, ResponseWithoutData, ResponseWithList, ResponseWithObject)

app = FastAPI(title="Real Estate Listings API")

properties = []

@app.get("/", response_model=ResponseWithoutData)
def home():
    return {
        "status": True,
        "message" : "Welcome to Real Estate Listings API"
    }

@app.get("/properties", response_model=ResponseWithList)
def get_properties():
    return {
        "status": True,
        "message" : "Properties fetched successfully",
        "properties": properties
    }

@app.get("/properties/{property_id}", response_model=ResponseWithObject)
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


@app.get("/search", response_model=ResponseWithList)
def search_properties(city: str = Query(min_length=2)):    
    properties_list = [item for item in properties if item["address"]["city"].lower() == city.lower()]

    return {
        "status": True,
        "message" : "Properties fetched successfully",
        "properties": properties_list
    }

@app.post(
    "/create-property", 
    response_model = PropertyResponse, 
    status_code = status.HTTP_201_CREATED
)
def create_property(property_data: PropertyCreate):
    new_property = property_data.model_dump()
    new_property["id"] = len(properties) + 1
    properties.append(new_property)
    return new_property