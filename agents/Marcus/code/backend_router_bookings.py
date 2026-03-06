from fastapi import APIRouter, Depends, HTTPException, Header, Request
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import uuid

router = APIRouter(prefix="/api/v1/bookings")

# Simple in-memory store for MVP demo
_BOOKINGS = {}

class BookingRequest(BaseModel):
    listing_id: str
    check_in: Optional[str]
    check_out: Optional[str]
    guests: Optional[int] = 1
    guest_checkout: Optional[bool] = False
    email: Optional[EmailStr]
    payment_method: str
    meta: Optional[dict] = None

class BookingResponse(BaseModel):
    booking_id: str
    status: str
    booking_token: str


async def get_current_user(request: Request):
    # placeholder for real auth
    auth = request.headers.get('authorization')
    if not auth:
        return None
    return {"user_id": "user-123"}


@router.post("/", response_model=BookingResponse, status_code=201)
async def create_booking(
    booking: BookingRequest,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
    current_user: Optional[dict] = Depends(get_current_user),
):
    # Guest checkout allowed: require email when guest_checkout=True and no user
    if booking.guest_checkout and not current_user:
        if not booking.email:
            raise HTTPException(status_code=400, detail="email required for guest checkout")
    # require auth OR guest_checkout
    if not current_user and not booking.guest_checkout:
        raise HTTPException(status_code=401, detail="authentication required or enable guest_checkout")

    # Idempotency: simple dedupe by idempotency_key
    if idempotency_key:
        existing = next((b for b in _BOOKINGS.values() if b.get('idempotency_key') == idempotency_key), None)
        if existing:
            return BookingResponse(
                booking_id=existing['booking_id'],
                status=existing['status'],
                booking_token=existing['booking_token'],
            )

    booking_id = str(uuid.uuid4())
    booking_token = str(uuid.uuid4())
    record = booking.dict()
    record.update({
        'booking_id': booking_id,
        'status': 'confirmed',
        'booking_token': booking_token,
        'idempotency_key': idempotency_key,
    })
    _BOOKINGS[booking_id] = record
    return BookingResponse(booking_id=booking_id, status='confirmed', booking_token=booking_token)


@router.get("/{booking_id}")
async def get_booking(booking_id: str, current_user: Optional[dict] = Depends(get_current_user)):
    record = _BOOKINGS.get(booking_id)
    if not record:
        raise HTTPException(status_code=404, detail="not found")
    # ownership check: if booking has email/user and current_user mismatch -> 403
    if current_user and record.get('user_id') and record.get('user_id') != current_user.get('user_id'):
        raise HTTPException(status_code=403, detail="forbidden")
    return record
