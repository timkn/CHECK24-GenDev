from datetime import datetime, date

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from app import models, schemas, crud, controller
from app.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [
	"http://localhost:5173",
	"http://localhost:5174"
	"http://localhost",
	"http://localhost:8000",
	"http://localhost:3000",
	"http://localhost:8080",
]

# For testing all origins are allowed
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
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


@app.get("/gpt_destination_search")
def ai_search(user_promt: str):
	gpt_response: dict = controller.gpt_destination_search(user_promt)
	if gpt_response is None:
		raise HTTPException(status_code=404, detail="gpt_destination_search failure")
	return {"response": gpt_response}


@app.get("/gpt_destination_description")
def ai_search(destination: str, outbounddeparturedatetime: date,
			  inboundarrivaldatetime: date, count_adults: int, count_children: int):
	gpt_response: str = controller.gpt_destination_description(destination, outbounddeparturedatetime,
															   inboundarrivaldatetime, count_adults, count_children)

	if gpt_response is None:
		raise HTTPException(status_code=404, detail="gpt_destination_description failure")
	return {"response": gpt_response}


@app.get("/offers")
def search_offers(airport: str, date_from: date, date_to: date, duration: int, count_adults: int, count_children: int,
				  db: Session = Depends(get_db)):
	offers = crud.get_offers_new(db, date_from, date_to, count_adults, count_children, airport, duration)

	if offers is None:
		raise HTTPException(status_code=404, detail="Offers not found")

	return offers


@app.get("/hotel/{hotel_id}/offers")
def search_offers(hotel_id: int, airport: str, date_from: date, date_to: date, duration: int, count_adults: int,
				  count_children: int,
				  db: Session = Depends(get_db)):
	offers = crud.get_offers_from_hotel(db, date_from, date_to, count_adults, count_children, airport, duration,
										hotel_id)

	if offers is None:
		raise HTTPException(status_code=404, detail="Offers not found")

	return offers


@app.get("/hotel/{hotel_id}/orm")
def search_offers(hotel_id: int, airport: str, date_from: date, date_to: date, duration: int, count_adults: int,
				  count_children: int,
				  db: Session = Depends(get_db)):
	offers = crud.get_offers_from_hotel_orm(db, date_from, date_to, count_adults, count_children, airport, duration,
											hotel_id)

	if offers is None:
		raise HTTPException(status_code=404, detail="Offers not found")

	return offers
