from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.session import get_db

app = FastAPI(title="Real Estate Listings API")

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):

    db_name = db.execute(
        text("SELECT current_database()")
    ).scalar_one()
    
    return {
        "status": True,
        "message" : "Welcome to Real Estate Listings API",
        "database" : db_name
    }

