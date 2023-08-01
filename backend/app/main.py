from datetime import datetime, date

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app import models, schemas, crud, controller
from app.database import engine, SessionLocal

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
import redis
models.Base.metadata.create_all(bind=engine)

CACHE_TIME = 120*60 # min * sec = 2h


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


@app.get("/")
def welcome():
	return RedirectResponse("/docs", status_code=303)


@app.on_event("startup")
async def startup():
	redis_instance = redis.Redis(host='localhost', port=6379, username='default',
								 password='jfhuez8f32fhfqnbef8g29hqnf024', decode_responses=False)
	FastAPICache.init(RedisBackend(redis_instance), prefix="fastapi-cache")


@app.get("/gpt_destination_search")
@cache(expire=CACHE_TIME)
def ai_search(user_promt: str):
	gpt_response: dict = controller.gpt_destination_search(user_promt)
	if gpt_response is None:
		raise HTTPException(status_code=404, detail="gpt_destination_search failure")
	return {"response": gpt_response}


@app.get("/gpt_destination_description")
@cache(expire=CACHE_TIME)
def destination_description(destination: str, outbounddeparturedatetime: date,
			  inboundarrivaldatetime: date, count_adults: int, count_children: int) -> dict:
	gpt_response: str = controller.gpt_destination_description(destination, outbounddeparturedatetime,
															   inboundarrivaldatetime, count_adults, count_children)

	if gpt_response is None:
		raise HTTPException(status_code=404, detail="gpt_destination_description failure")
	return {"response": gpt_response}


@app.get("/offers")
@cache(expire=CACHE_TIME)
def search_offers(airport: str, date_from: date, date_to: date, duration: int, count_adults: int, count_children: int,
				  db: Session = Depends(get_db)):
	offers = crud.get_offers_new(db, date_from, date_to, count_adults, count_children, airport, duration)

	if offers is None:
		raise HTTPException(status_code=404, detail="Offers not found")

	return offers


@app.get("/hotel/{hotel_id}/offers")
@cache(expire=CACHE_TIME)
def search_offers(hotel_id: int, airport: str, date_from: date, date_to: date, duration: int, count_adults: int,
				  count_children: int,
				  db: Session = Depends(get_db)):
	offers = crud.get_offers_from_hotel(db, date_from, date_to, count_adults, count_children, airport, duration,
										hotel_id)

	if offers is None:
		raise HTTPException(status_code=404, detail="Offers not found")

	return offers
