from fastapi import FastAPI

app = FastAPI(title="Real Estate Listings API")

properties = [
    {
        "id": 1,
        "title": "Modern 2 BHK Apartment",
        "city": "Indore",
        "price": 4500000,
        "property_type": "Apartment",
    },
    {
        "id": 2,
        "title": "Independent Family House",
        "city": "Bhopal",
        "price": 7500000,
        "property_type": "House",
    },
    {
        "id": 3,
        "title": "Affordable 1 BHK Flat",
        "city": "Indore",
        "price": 2500000,
        "property_type": "Apartment",
    }
]

@app.get("/")
def home():
    return {
        "status": True,
        "message" : "Welcome to Real Estate Listings API"
    }

@app.get("/properties")
def get_properties():
    return {
        "status": True,
        "message" : "Properties fetched successfully",
        "properties": properties
    }

@app.get("/properties/{property_id}")
def get_property(property_id: int):
    property = None
    for item in properties:
        if item["id"] == property_id:
            property = item

    if property is None:
        return {
            "status": False,
            "message" : "Failed to fetch property",
        }
    else:
        return {
            "status": True,
            "message" : "Property fetched successfully",
            "property": property
        }


@app.get("/search")
def search_properties(city: str | None = None):
    if city is None:
        return {
            "status": False,
            "message" : "Bad Request",
        }
    
    properties_list = [item for item in properties if item["city"].lower() == city.lower()]

    return {
        "status": True,
        "message" : "Properties fetched successfully",
        "properties": properties_list
    }