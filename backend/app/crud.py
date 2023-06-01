from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import timedelta, date, datetime

from app import models, schemas


def get_hotel(db: Session, hotel_id: int):
	return db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()


def get_offers(db: Session, date_from: date, date_to: date, count_adults: int, count_children: int, airport: str, duration: int):

	sql = f"""
		select distinct min(price) as min, *
		FROM offers_1, hotels
		where outbounddeparturedatetime >= '{date_from}'
		AND inboundarrivaldatetime <= '{date_to}'
		AND countadults={count_adults} AND countchildren={count_children}
		AND outbounddepartureairport='{airport}'
		and hotels.id = offers_1.hotelid
		AND date_trunc('day', inboundarrivaldatetime) - date_trunc('day', outbounddeparturedatetime) = interval '{duration} days'
		group by hotelid, outbounddeparturedatetime, inbounddeparturedatetime, countadults, countchildren, price, inbounddepartureairport, outboundarrivalairport, inboundarrivaldatetime, outbounddepartureairport, inboundarrivalairport, outboundarrivaldatetime, mealtype, oceanview, roomtype, id, name, stars
		order by min;
		"""

	res = db.execute(text(sql))


	print(res)
	result_set = res.fetchall()

	results = []
	for row in result_set:
		result = {
			'min': row[0],
			'hotelid': row[1],
			'outbounddeparturedatetime': row[2],
			'inbounddeparturedatetime': row[3],
			'countadults': row[4],
			'countchildren': row[5],
			'price': row[6],
			'inbounddepartureairport': row[7],
			'inboundarrivalairport': row[8],
			'inboundarrivaldatetime': row[9],
			'outbounddepartureairport': row[10],
			'outboundarrivalairport': row[11],
			'outboundarrivaldatetime': row[12],
			'mealtype': row[13],
			'oceanview': bool(row[14]),
			'roomtype': row[15],
			'hotel': {
				'id': row[16],
				'name': row[17],
				'stars': row[18]
			}
		}
		results.append(result)
	print(results)
	return results