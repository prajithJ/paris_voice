from fastapi import FastAPI
from pydantic import BaseModel

from supabase_service import save_booking

app = FastAPI()


class BookingRequest(BaseModel):
    customer_name: str
    customer_phone: str
    appointment_time: str
    service_type: str
    calendar_event_id: str


@app.get("/")
def root():
    return {"status": "running"}


@app.post("/booking-created")
def booking_created(req: BookingRequest):

    save_booking(
        customer_name=req.customer_name,
        customer_phone=req.customer_phone,
        appointment_time=req.appointment_time,
        service_type=req.service_type,
        calendar_event_id=req.calendar_event_id
    )

    return {
        "success": True,
        "message": "Booking stored"
    }

@app.get("/health")
def health():
    return {"status": "ok"}