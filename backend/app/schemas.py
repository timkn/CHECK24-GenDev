from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class MealTypeEnum(str, Enum):
    BREAKFAST = 'Breakfast'
    LUNCH = 'Lunch'
    DINNER = 'Dinner'


class BookingBase(BaseModel):
    hotel_id: int
    flight_id: int
    count_adults: int
    count_children: int
    price: float
    meal_type: Optional[MealTypeEnum]


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BookingBase):
    pass


class Booking(BaseModel):
    id: int
    hotel: "Hotel"
    flight: "Flight"

    class Config:
        orm_mode = True


class HotelBase(BaseModel):
    name: str
    stars: int


class HotelCreate(HotelBase):
    pass


class HotelUpdate(HotelBase):
    pass


class Hotel(BaseModel):
    id: int
    stars: int
    name: str
    rooms: list["Room"]
    offers: list[Booking]

    class Config:
        orm_mode = True


class FlightBase(BaseModel):
    departure_airport: str
    arrival_airport: str
    departure_datetime: datetime
    arrival_datetime: datetime


class FlightCreate(FlightBase):
    pass


class FlightUpdate(FlightBase):
    pass


class Flight(BaseModel):
    id: int
    departure_airport: str
    arrival_airport: str
    departure_datetime: datetime
    arrival_datetime: datetime
    offers: list[Booking]

    class Config:
        orm_mode = True


class RoomBase(BaseModel):
    hotel_id: int
    type: str
    ocean_view: Optional[bool]


class RoomCreate(RoomBase):
    pass


class RoomUpdate(RoomBase):
    pass


class Room(BaseModel):
    id: int
    hotel_id: int
    type: str
    ocean_view: Optional[bool]
    hotel: Hotel
    offers: list[Booking]

    class Config:
        orm_mode = True
