from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud, controller
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
    query = controller.ai_search(query)
    if query is None:
        raise HTTPException(status_code=404, detail="search failure")

    return {query}


@app.get("/hotels/{hotel_id}", response_model=schemas.Hotel)
def read_hotel(hotel_id: int, db: Session = Depends(get_db)):
    db_hotel = crud.get_hotel(db, hotel_id=hotel_id)
    if db_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return db_hotel
