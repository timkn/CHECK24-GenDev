from sqlalchemy import Column, Integer, String, DateTime, Float, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    stars = Column(Integer)
    offers = relationship("Offer", back_populates="hotel")


class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    outbounddeparturedatetime = Column(DateTime)
    inbounddeparturedatetime = Column(DateTime)
    countadults = Column(Integer)
    countchildren = Column(Integer)
    price = Column(Float)
    inbounddepartureairport = Column(String)
    inboundarrivalairport = Column(String)
    inboundarrivaldatetime = Column(DateTime)
    outbounddepartureairport = Column(String)
    outboundarrivalairport = Column(String)
    outboundarrivaldatetime = Column(DateTime)
    meal_type = Column(String)
    oceanview = Column(Boolean)
    roomtype = Column(String)
    hotel = relationship("Hotel", back_populates="offers")

