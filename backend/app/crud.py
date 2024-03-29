from sqlalchemy import text, func
from sqlalchemy.orm import Session
from datetime import timedelta, date, datetime


def get_offers_from_hotel(db: Session, date_from: date, date_to: date, count_adults: int, count_children: int,
						  airport: str,
						  duration: int, hotelid: int):
	SQL_OFFERS_FROM_HOTEL = f"""
	select distinct *
		FROM offers, hotels
		where outbounddeparturedatetime >= :date_from
		AND inboundarrivaldatetime <= :date_to
		AND hotelid = :hotelid
		AND countadults=:count_adults AND countchildren=:count_children
		AND outbounddepartureairport=:airport
		AND hotels.id = offers.hotelid
		AND date_trunc('day', inboundarrivaldatetime) - date_trunc('day', outbounddeparturedatetime) = ':duration days';
	"""
	res = db.execute(text(SQL_OFFERS_FROM_HOTEL), {"date_from":date_from, "date_to":date_to, "hotelid":hotelid, "count_adults":count_adults, "count_children":count_children, "airport":airport, "duration":duration})

	result_set = res.fetchall()

	print("received offers hotel from db")

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
			where outbounddeparturedatetime >= :date_from
			AND inboundarrivaldatetime <= :date_to
			AND countadults=:count_adults AND countchildren=:count_children
			AND outbounddepartureairport=:airport
			AND date_trunc('day', inboundarrivaldatetime) - date_trunc('day', outbounddeparturedatetime) = interval ':duration days'
			and h.id = o.hotelid
			group by h.id
			order by min;
			"""

	res = db.execute(text(sql), {"date_from":date_from, "date_to":date_to, "count_adults":count_adults, "count_children":count_children, "airport":airport, "duration":duration })

	result_set = res.fetchall()

	print("received offers from db")

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

