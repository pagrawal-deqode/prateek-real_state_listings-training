from fastapi import FastAPI
from schemas.property import (ResponseWithoutData)
from routers import properties, extras

app = FastAPI(title="Real Estate Listings API")

app.include_router(properties.router, prefix="/properties", tags=["Properties"])
app.include_router(extras.router, prefix="/extras", tags=["Extras"])

@app.get("/", response_model=ResponseWithoutData)
def home():
    return {
        "status": True,
        "message" : "Welcome to Real Estate Listings API"
    }

