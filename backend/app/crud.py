from collections import defaultdict

from sqlalchemy import text, func
from sqlalchemy.orm import Session
from datetime import timedelta, date, datetime

from app import models, schemas
from app.models import Offer, Hotel

def get_all_offer_from_hotel(db: Session, hotelid:int):
	query = db.query(Offer).filter(Offer.hotelid == hotelid).limit(10)

	results = query.all()

	return results

def get_offers_from_hotel_orm(db: Session, date_from: date, date_to: date, count_adults: int, count_children: int, airport: str, duration: int, hotelid: int):
	query = db.query(Offer).distinct().join(Hotel).filter(
		Offer.outbounddeparturedatetime >= date_from,
		Offer.inboundarrivaldatetime <= date_to,
		Offer.hotelid == hotelid,
		Offer.countadults == count_adults,
		Offer.countchildren == count_children,
		Offer.outbounddepartureairport == airport,
		Hotel.id == Offer.hotelid,
		text("date_trunc('day', offers_1.inboundarrivaldatetime) - date_trunc('day', offers_1.outbounddeparturedatetime) = interval '{}'".format(duration))
	)

	results = query.all()

	for i in results:
		print(i)

	return results

def get_offers_from_hotel(db: Session, date_from: date, date_to: date, count_adults: int, count_children: int,
						  airport: str,
						  duration: int, hotelid: int):
	sql = f"""
	select distinct *
		FROM offers_1, hotels
		where outbounddeparturedatetime >= '{date_from}'
		AND inboundarrivaldatetime <= '{date_to}'
		AND hotelid = {hotelid}
		AND countadults={count_adults} AND countchildren={count_children}
		AND outbounddepartureairport='{airport}'
		AND hotels.id = offers_1.hotelid
		AND date_trunc('day', inboundarrivaldatetime) - date_trunc('day', outbounddeparturedatetime) = '{duration} days';
	"""
	res = db.execute(text(sql))

	result_set = res.fetchall()

	print("received res from db")

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
			'outboundarrivalairport': row[7],
			'inboundarrivaldatetime': row[8],
			'outbounddepartureairport': row[9],
			'inboundarrivalairport': row[10],
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


def get_offers_new(db: Session, date_from: date, date_to: date, count_adults: int, count_children: int, airport: str,
				   duration: int):
	sql = f"""
			select h.*, min(o.price) as min from hotels h, offers o
			where outbounddeparturedatetime >= '{date_from}'
			AND inboundarrivaldatetime <= '{date_to}'
			AND countadults={count_adults} AND countchildren={count_children}
			AND outbounddepartureairport='{airport}'
			AND date_trunc('day', inboundarrivaldatetime) - date_trunc('day', outbounddeparturedatetime) = interval '{duration} days'
			and h.id = o.hotel_id
			group by h.id
			order by min;
			"""

	res = db.execute(text(sql))

	result_set = res.fetchall()

	print("received res from db")

	results = []
	for row in result_set:
		result = {
			'id': row[0],
			'name': row[1],
			'starts': row[2],
			'price': row[3],
		}
		results.append(result)

	return results


def get_offers(db: Session, date_from: date, date_to: date, count_adults: int, count_children: int, airport: str,
			   duration: int):
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

	result_set = res.fetchall()

	print("received res from db")

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
			'outboundarrivalairport': row[8],
			'inboundarrivaldatetime': row[9],
			'outbounddepartureairport': row[10],
			'inboundarrivalairport': row[11],
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
	return results
