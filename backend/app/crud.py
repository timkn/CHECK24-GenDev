from sqlalchemy.orm import Session

from app import models, schemas


def get_hotel(db: Session, hotel_id: int):
    return db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()


def get_offers(db: Session, hotel_id: int):
    return db.query(models.Offery).filter(models.Offer.hotel_id == hotel_id).all()
