from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class PlaceBase(BaseModel):
    id: str
    name: str
    city: Optional[str]
    country: Optional[str]
    lat: float
    lon: float
    tags: List[str] = []
    rating: Optional[float]

class DiscoveryResponse(BaseModel):
    featured: List[PlaceBase]
    promos: List[dict] = []

class SearchResponse(BaseModel):
    total: int
    items: List[PlaceBase]

class ItineraryCreate(BaseModel):
    title: str
    start_date: Optional[date]
    end_date: Optional[date]

class ItineraryUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]

class ItineraryItem(BaseModel):
    place_id: str
    day_index: int
    start_time: Optional[str]
    end_time: Optional[str]
    notes: Optional[str]

class Itinerary(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    start_date: Optional[date]
    end_date: Optional[date]
    items: List[ItineraryItem] = []

class BookingCreate(BaseModel):
    itinerary_id: Optional[str]
    provider: str
    amount_cents: int
    currency: str

class Booking(BaseModel):
    id: str
    status: str
    amount_cents: int
    currency: str

