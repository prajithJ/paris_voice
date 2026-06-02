from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SECRET_KEY
)


def save_booking(
    customer_name,
    customer_phone,
    appointment_time,
    service_type,
    calendar_event_id
):
    data = {
        "customer_name": customer_name,
        "customer_phone": customer_phone,
        "appointment_time": appointment_time,
        "service_type": service_type,
        "calendar_event_id": calendar_event_id
    }

    result = supabase.table("bookings").insert(data).execute()

    return result