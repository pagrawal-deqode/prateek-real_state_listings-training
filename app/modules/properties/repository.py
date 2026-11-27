from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.properties.models import Property

def create_property(db: Session, property_data: dict):
    property_obj = Property(**property_data)

    db.add(property_obj)
    db.commit()
    db.refresh(property_obj)

    return property_obj


def get_all_properties(db: Session, skip: int = 0, limit: int = 10):
    statement = (
        select(Property).order_by(Property.id.desc()).offset(skip).limit(limit)
    )

    return db.scalars(statement).all()


def get_property_by_id(db: Session, property_id: int):
    statement = (
        select(Property).where(Property.id == property_id)
    )

    return db.scalar(statement)


def update_property(db: Session, property_obj: Property, update_data: dict):
    for field, value in update_data.items():
        setattr(property_obj, field, value)

    db.commit()
    db.refresh(property_obj)

    return property_obj

def delete_property(db:Session, property_obj: Property):
    db.delete(property_obj)
    db.commit()
