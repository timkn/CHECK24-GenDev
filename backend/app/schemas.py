from datetime import datetime
from pydantic import BaseModel


class HotelBase(BaseModel):
    name: str
    stars: int

class HotelCreate(HotelBase):
    pass

class Hotel(HotelBase):
    id: int

    class Config:
        orm_mode = True


class OfferBase(BaseModel):
    outbounddeparturedatetime: str
    inbounddeparturedatetime: str
    countadults: int
    countchildren: int
    price: int
    inbounddepartureairport: str
    inboundarrivalairport: str
    inboundarrivaldatetime: str
    outbounddepartureairport: str
    outboundarrivalairport: str
    outboundarrivaldatetime: str
    meal_type: str
    oceanview: bool
    roomtype: str

class OfferCreate(OfferBase):
    hotelid: int

class Offer(OfferBase):
    hotelid: int


    class Config:
        orm_mode = True