from datetime import datetime, date

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import DateTime
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from app import models, schemas, crud, controller
from app.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
	"http://localhost:5173",
	"http://localhost",
	"http://localhost:8000",
	"http://localhost:3000",
	"http://localhost:8080",
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


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
	return {"response": query}


@app.get("/hotels/{hotel_id}/offers", response_model=schemas.Hotel)
def read_hotel(hotel_id: int, db: Session = Depends(get_db)):
	db_hotel = crud.get_hotel(db, hotel_id=hotel_id)
	if db_hotel is None:
		raise HTTPException(status_code=404, detail="Hotel not found")
	return db_hotel


@app.get("/offers")
def search_offers(airport: str, date_from: date, date_to: date, duration: int, count_adults: int, count_children: int,
				  db: Session = Depends(get_db)):
	offers = crud.get_offers(db, date_from, date_to, count_adults, count_children, airport, duration)

	if offers is None:
		raise HTTPException(status_code=404, detail="Offers not found")

	return offers
