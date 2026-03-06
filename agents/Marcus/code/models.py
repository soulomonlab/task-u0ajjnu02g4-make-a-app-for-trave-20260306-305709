from datetime import datetime
import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
    Float,
    ForeignKey,
    Table,
    JSON,
    Boolean,
    Index,
    ARRAY,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    hashed_password = Column(String(255), nullable=True)
    role = Column(String(50), default='user')
    created_at = Column(DateTime, default=datetime.utcnow)

class Place(Base):
    __tablename__ = 'places'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    city = Column(String(100), index=True)
    country = Column(String(100), index=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    tags = Column(ARRAY(String), default=[])
    rating = Column(Float, default=0.0)
    metadata = Column(JSON, default={})

    __table_args__ = (
        Index('ix_places_tags', 'tags', postgresql_using='gin'),
    )

class Itinerary(Base):
    __tablename__ = 'itineraries'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    status = Column(String(50), default='draft')
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User')
    items = relationship('ItineraryItem', back_populates='itinerary', cascade='all, delete-orphan')

class ItineraryItem(Base):
    __tablename__ = 'itinerary_items'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itinerary_id = Column(UUID(as_uuid=True), ForeignKey('itineraries.id'), nullable=False)
    place_id = Column(UUID(as_uuid=True), ForeignKey('places.id'), nullable=False)
    day_index = Column(Integer, nullable=False, default=0)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)

    itinerary = relationship('Itinerary', back_populates='items')
    place = relationship('Place')

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    itinerary_id = Column(UUID(as_uuid=True), ForeignKey('itineraries.id'), nullable=True)
    provider = Column(String(255), nullable=False)
    provider_booking_id = Column(String(255), nullable=True)
    status = Column(String(50), default='pending')
    amount_cents = Column(Integer, nullable=False)
    currency = Column(String(10), default='USD')
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User')

