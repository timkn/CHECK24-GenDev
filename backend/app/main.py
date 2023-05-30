from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.get("/aisearch")
def ai_search(query: str):
    return {"query": query}



@app.post("/hotels/")
def create_hotel(hotel: schemas.HotelCreate, db: Session = Depends(get_db)):
    db_hotel = crud.create_hotel(db, hotel)
    return db_hotel


@app.get("/hotels/{hotel_id}")
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    db_hotel = crud.get_hotel(db, hotel_id)
    if db_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return db_hotel


@app.get("/hotels/")
def get_hotels(db: Session = Depends(get_db)):
    db_hotels = crud.get_hotels(db)
    return db_hotels


@app.put("/hotels/{hotel_id}")
def update_hotel(hotel_id: int, hotel: schemas.HotelUpdate, db: Session = Depends(get_db)):
    db_hotel = crud.update_hotel(db, hotel_id, hotel)
    if db_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return db_hotel


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    db_hotel = crud.delete_hotel(db, hotel_id)
    if db_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return db_hotel


# Booking Endpoints

@app.post("/offers/")
def create_offer(offer: schemas.BookingCreate, db: Session = Depends(get_db)):
    db_offer = crud.create_offer(db, offer)
    return db_offer


@app.get("/offers/{offer_id}")
def get_offer(offer_id: int, db: Session = Depends(get_db)):
    db_offer = crud.get_offer(db, offer_id)
    if db_offer is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_offer


@app.get("/offers/")
def get_offers(db: Session = Depends(get_db)):
    db_offers = crud.get_offers(db)
    return db_offers


@app.put("/offers/{offer_id}")
def update_offer(offer_id: int, offer: schemas.BookingUpdate, db: Session = Depends(get_db)):
    db_offer = crud.update_offer(db, offer_id, offer)
    if db_offer is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_offer


@app.delete("/offers/{offer_id}")
def delete_offer(offer_id: int, db: Session = Depends(get_db)):
    db_offer = crud.delete_offer(db, offer_id)
    if db_offer is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_offer


# Room Endpoints

@app.post("/rooms/")
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    db_room = crud.create_room(db, room)
    return db_room
