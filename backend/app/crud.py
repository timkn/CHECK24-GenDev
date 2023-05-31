from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import timedelta, date, datetime

from app import models, schemas


def get_hotel(db: Session, hotel_id: int):
	return db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()


def get_offers(db: Session, date_from: date, date_to: date, count_adults: int, count_children: int, airport: str, duration: int):
	date_from_timestamp = date_from
	date_to_timestamp = date_to


	print("date_from_timestamp = ", date_from_timestamp)
	print("date_to_timestamp = ", date_to_timestamp)



	sql = f"""
		SELECT *
		FROM offers_1, hotels
		WHERE outbounddeparturedatetime BETWEEN '{date_from_timestamp}' AND '{date_to_timestamp}'
		AND inboundarrivaldatetime BETWEEN '{date_from_timestamp}' AND '{date_to_timestamp}'
		AND countadults={count_adults} AND countchildren={count_children}
		AND outbounddepartureairport='{airport}'
		AND offers_1.hotelid = hotels.id
		AND date_trunc('day', inboundarrivaldatetime) - date_trunc('day', outbounddeparturedatetime) = interval '{duration} days';
		"""

	res = db.execute(text(sql))


	print(res)
	result_set = res.fetchall()

	results = []
	for row in result_set:
		result = {
			'hotelid': row[0],
			'outbounddeparturedatetime': row[1],
			'inbounddeparturedatetime': row[2],
			'countadults': row[3],
			'countchildren': row[4],
			'price': row[5],
			'inbounddepartureairport': row[6],
			'inboundarrivalairport': row[7],
			'inboundarrivaldatetime': row[8],
			'outbounddepartureairport': row[9],
			'outboundarrivalairport': row[10],
			'outboundarrivaldatetime': row[11],
			'mealtype': row[12],
			'oceanview': bool(row[13]),
			'roomtype': row[14],
			'hotel': {
				'id': row[15],
				'name': row[16],
				'stars': row[17]
			}
		}
		results.append(result)
	return results




def get_offers_2(db: Session, date_from: str, date_to: str, count_adults: int, count_children: int, airport: str,
				 duration: int):
	return db.query(models.Offer).limit(10)
