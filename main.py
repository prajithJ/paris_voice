from fastapi import FastAPI, Request
from pydantic import BaseModel

from supabase_service import save_booking, get_client_id_for_assistant

app = FastAPI()


class BookingRequest(BaseModel):
    customer_name: str
    customer_phone: str
    appointment_time: str
    service_type: str


@app.get("/")
def root():
    return {"status": "running"}


@app.post("/booking-created")
async def booking_created(request: Request):

    body = await request.json()

    print("BODY RECEIVED")
    print(body)

    message = body["message"]

    args = message["toolCalls"][0]["function"]["arguments"]

    print("ARGS")
    print(args)

    # Figure out which client this call belongs to, based on which
    # Vapi assistant handled it. Check a couple of likely payload
    # locations since we haven't confirmed the exact field yet.
    assistant_id = None
    if message.get("assistant"):
        assistant_id = message["assistant"].get("id")
    if not assistant_id and message.get("call"):
        assistant_id = message["call"].get("assistantId")

    print("ASSISTANT ID")
    print(assistant_id)

    client_id = get_client_id_for_assistant(assistant_id)

    if client_id is None:
        print("WARNING: no client matched for assistant_id — falling back to DEFAULT_CLIENT_ID")

    save_booking(
        customer_name=args["customer_name"],
        customer_phone=args["customer_phone"],
        appointment_time=args["appointment_time"],
        service_type=args["service_type"],
        client_id=client_id
    )

    print("BOOKING SAVED")

    return {
        "success": True,
        "message": "Booking stored"
    }

@app.get("/health")
def health():
    return {"status": "ok"}