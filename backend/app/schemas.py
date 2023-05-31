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
    outbounddeparturedatetime: datetime
    inbounddeparturedatetime: datetime
    countadults: int
    countchildren: int
    price: float
    inbounddepartureairport: str
    inboundarrivalairport: str
    inboundarrivaldatetime: str
    outbounddepartureairport: str
    outboundarrivalairport: str
    outboundarrivaldatetime: datetime
    meal_type: str
    oceanview: bool
    roomtype: str

class OfferCreate(OfferBase):
    hotel_id: int

class Offer(OfferBase):
    id: int
    hotel_id: int


    class Config:
        orm_mode = True