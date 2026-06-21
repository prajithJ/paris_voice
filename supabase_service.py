from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")
DEFAULT_CLIENT_ID = os.getenv("DEFAULT_CLIENT_ID")  # last-resort fallback only

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SECRET_KEY
)


def get_client_id_for_assistant(assistant_id):
    """Look up which client owns this Vapi assistant. Returns None if no match."""
    if not assistant_id:
        return None

    result = (
        supabase.table("clients")
        .select("id")
        .eq("vapi_assistant_id", assistant_id)
        .execute()
    )

    if result.data:
        return result.data[0]["id"]

    return None


def save_booking(
    customer_name,
    customer_phone,
    appointment_time,
    service_type,
    client_id=None,
):
    data = {
        "client_id": client_id or DEFAULT_CLIENT_ID,
        "customer_name": customer_name,
        "customer_phone": customer_phone,
        "appointment_time": appointment_time,
        "service_type": service_type
    }

    result = supabase.table("bookings").insert(data).execute()

    return result