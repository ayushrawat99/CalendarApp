from datetime import datetime, timedelta
from google.cloud import firestore
import pytz

def convert_to_timezone(datetime_str):
    dt_object = datetime.datetime.fromisoformat()

    # Convert to Firestore timestamp
    timestamp = firestore.Timestamp(dt_object)

    # Logic to convert datetime from one timezone to another
    return timestamp

def parse_datetime(date_str):
    """
    Convert a date string to a UTC datetime object.
    Assumes ISO 8601 format (e.g., "2024-10-01T00:00:00").
    """
    try:
        # Convert to UTC datetime
        return datetime.fromisoformat(date_str).replace(tzinfo=pytz.UTC)
    except ValueError:
        raise ValueError("Invalid date format. Use ISO 8601 format.")