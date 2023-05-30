from sqlalchemy import Column, Integer, String, DateTime, Float, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    stars = Column(Integer)
    rooms = relationship("Room", back_populates="hotel")


class Flight(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    departure_airport = Column(String)
    arrival_airport = Column(String)
    departure_datetime = Column(DateTime)
    arrival_datetime = Column(DateTime)
    offers = relationship("Booking", back_populates="flight")


class Offer(Base):
    __tablename__ = 'offers'

    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    flight_id = Column(Integer, ForeignKey('flights.id'))
    count_adults = Column(Integer)
    count_children = Column(Integer)
    price = Column(Float)
    meal_type = Column(Enum("BREAKFAST", "ALLINCLUSIVE", "HALFBOARD", "NONE", name="meal_type_enum"), nullable=False)
    hotel = relationship("Hotel", back_populates="offers")
    flight = relationship("Flight", back_populates="offers")


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    type = Column(Enum("APARTMENT", "DOUBLE", "STUDIO", "FAMILY", "SUITE", "SINGLE", "ACCORDINGDESCRIPTION", name="room_type_enum"))
    ocean_view = Column(Boolean)
    offers = relationship("Booking", back_populates="room")
