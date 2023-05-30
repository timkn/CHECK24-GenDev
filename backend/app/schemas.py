from datetime import datetime
from pydantic import BaseModel


class HotelBase(BaseModel):
    id: int
    name: str
    stars: int


class HotelCreate(HotelBase):
    pass


class Hotel(HotelBase):
    class Config:
        orm_mode = True


class OfferBase(BaseModel):
    hotel_id: int
    outbounddeparturedatetime: datetime
    inbounddeparturedatetime: datetime
    countadults: int
    countchildren: int
    price: float
    inbounddepartureairport: str
    inboundarrivalairport: str
    inboundarrivaldatetime: datetime
    outbounddepartureairport: str
    outboundarrivalairport: str
    outboundarrivaldatetime: datetime
    meal_type: str
    oceanview: bool
    roomtype: str


class OfferCreate(OfferBase):
    pass


class Offer(OfferBase):
    id: int

    class Config:
        orm_mode = True
