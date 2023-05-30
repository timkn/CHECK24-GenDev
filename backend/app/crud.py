from sqlalchemy.orm import Session

from app import models, schemas


def create_hotel(db: Session, hotel: schemas.HotelCreate):
    db_hotel = models.Hotel(name=hotel.name)
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel


def get_hotel(db: Session, hotel_id: int):
    return db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()


def get_hotels(db: Session):
    return db.query(models.Hotel).all()


def update_hotel(db: Session, hotel_id: int, hotel: schemas.HotelUpdate):
    db_hotel = db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()
    if db_hotel:
        db_hotel.name = hotel.name
        db.commit()
        db.refresh(db_hotel)
    return db_hotel


def delete_hotel(db: Session, hotel_id: int):
    db_hotel = db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()
    if db_hotel:
        db.delete(db_hotel)
        db.commit()
    return db_hotel


def create_offer(db: Session, offer: schemas.BookingCreate):
    db_offer = models.Offer(
        hotel_id=offer.hotel_id,
        flight_id=offer.flight_id,
        count_adults=offer.count_adults,
        count_children=offer.count_children,
        price=offer.price,
        meal_type=offer.meal_type
    )
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer


def get_offer(db: Session, offer_id: int):
    return db.query(models.Offer).filter(models.Offer.id == offer_id).first()


def get_offers(db: Session):
    return db.query(models.Offer).all()


def update_offer(db: Session, offer_id: int, offer: schemas.BookingUpdate):
    db_offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()
    if db_offer:
        db_offer.count_adults = offer.count_adults
        db_offer.count_children = offer.count_children
        db_offer.price = offer.price
        db_offer.meal_type = offer.meal_type
        db.commit()
        db.refresh(db_offer)
    return db_offer


def delete_offer(db: Session, offer_id: int):
    db_offer = db.query(models.Offer).filter(models.Offer.id == offer_id).first()
    if db_offer:
        db.delete(db_offer)
        db.commit()
    return db_offer


# Room Functions

def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(
        hotel_id=room.hotel_id,
        type=room.type,
        ocean_view=room.ocean_view
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()


def get_rooms(db: Session):
    return db.query(models.Room).all()


def update_room(db: Session, room_id: int, room: schemas.RoomUpdate):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if db_room:
        db_room.type = room.type
        db_room.ocean_view = room.ocean_view
        db.commit()
        db.refresh(db_room)
    return db_room


def delete_room(db: Session, room_id: int):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if db_room:
        db.delete(db_room)
        db.commit()
    return db_room


# Flight Functions

def create_flight(db: Session, flight: schemas.FlightCreate):
    db_flight = models.Flight(
        departure_airport=flight.departure_airport,
        arrival_airport=flight.arrival_airport,
        departure_datetime=flight.departure_datetime,
        arrival_datetime=flight.arrival_datetime
    )
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight


def get_flight(db: Session, flight_id: int):
    return db.query(models.Flight).filter(models.Flight.id == flight_id).first()


def get_flights(db: Session):
    return db.query(models.Flight).all()


def update_flight(db: Session, flight_id: int, flight: schemas.FlightUpdate):
    db_flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()
    if db_flight:
        db_flight.departure_airport = flight.departure_airport
        db_flight.arrival_airport = flight.arrival_airport
        db_flight.departure_datetime = flight.departure_datetime
        db_flight.arrival_datetime = flight.arrival_datetime
        db.commit()
        db.refresh(db_flight)
    return db_flight


def delete_flight(db: Session, flight_id: int):
    db_flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()
    if db_flight:
        db.delete(db_flight)
        db.commit()
    return db_flight
