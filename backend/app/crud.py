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
		FROM offers_1
		WHERE outbounddeparturedatetime BETWEEN '{date_from_timestamp}' AND '{date_to_timestamp}'
		AND inboundarrivaldatetime BETWEEN '{date_from_timestamp}' AND '{date_to_timestamp}'
		AND countadults={count_adults} AND countchildren={count_children}
		AND outbounddepartureairport='{airport}'
		AND date_trunc('day', inboundarrivaldatetime) - date_trunc('day', outbounddeparturedatetime) = interval '{duration} days';
		"""

	res = db.execute(text(sql))

	print("hay")
	print(res)
	result_set = res.fetchall()
	print(result_set)
	for row in result_set:
		id = row[0]
		outbound_departure_datetime = row[1]
		outbound_arrival_datetime = row[2]
		inbound_departure_datetime = row[3]
		inbound_arrival_datetime = row[4]
		countadults = row[5]
		countchildren = row[6]
		outbounddepartureairport = row[7]
		inboundarrivalairport = row[8]
		price = row[9]
		print(
			f"Offer ID: {id}, Outbound Departure Datetime: {outbound_departure_datetime}, Outbound Arrival Datetime: {outbound_arrival_datetime}, Price: {price}")


def get_offers_2(db: Session, date_from: str, date_to: str, count_adults: int, count_children: int, airport: str,
				 duration: int):

	outbound_departure_datetime = datetime.strptime(date_from, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
	inbound_arrival_datetime = datetime.strptime(date_to, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')

	inbound_departure_datetime = inbound_arrival_datetime - timedelta(days=duration)

	return db.query(models.Offer).join(models.Offer.hotel).filter(
		models.Offer.countadults == count_adults,
		models.Offer.countchildren == count_children,
		models.Offer.outbounddepartureairport == airport,
		models.Offer.outbounddeparturedatetime >= outbound_departure_datetime,
		models.Offer.outbounddeparturedatetime < outbound_departure_datetime + timedelta(days=1),
		models.Offer.inboundarrivaldatetime >= inbound_arrival_datetime,
		models.Offer.inboundarrivaldatetime < inbound_arrival_datetime + timedelta(days=1),
		models.Offer.inbounddeparturedatetime >= inbound_departure_datetime,
		models.Offer.inbounddeparturedatetime < inbound_departure_datetime + timedelta(days=1)
	).all()
