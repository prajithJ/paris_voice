from fastapi import FastAPI
from pydantic import BaseModel

from supabase_service import save_booking

app = FastAPI()


class BookingRequest(BaseModel):
    customer_name: str
    customer_phone: str
    appointment_time: str
    service_type: str


@app.get("/")
def root():
    return {"status": "running"}


from fastapi import Request

@app.post("/booking-created")
async def booking_created(request: Request):

    body = await request.json()

    args = body["message"]["toolCalls"][0]["function"]["arguments"]

    save_booking(
        customer_name=args["customer_name"],
        customer_phone=args["customer_phone"],
        appointment_time=args["appointment_time"],
        service_type=args["service_type"]
    )

    return {
        "success": True,
        "message": "Booking stored"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

from fastapi import Request

