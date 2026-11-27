from fastapi import FastAPI

from app.modules.properties.router import router as properties_router

app = FastAPI(
    title="Real Estate Listings API",
    description="API for managing real estate property listings",
    version="1.0.0"
)

app.include_router(properties_router)

@app.get("/health")
def health():
    return {
        "status": True,
        "message" : "Welcome to Real Estate Listings API",
    }