from datetime import datetime, timedelta
import pytz
import firebase_admin
from firebase_admin import credentials, firestore
from flask import jsonify

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase_config_credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Constants
START_HOUR = 10
END_HOUR = 17
SLOT_DURATION_MINUTES = 30  # Duration of each slot in minutes
BASE_TIMEZONE = 'Asia/Tokyo'

class EventsService:

    @staticmethod
    def create_event(data):
        """
        Create an event in Firestore.
        """
        try:
            # Parse event datetime and duration
            event_datetime = datetime.fromisoformat(data['datetime'])
            event_duration = int(data['duration'])
            
            # Convert to UTC and store as Unix timestamp
            local_tz = pytz.timezone(BASE_TIMEZONE)
            localized_event_datetime = local_tz.localize(event_datetime)
            utc_event_datetime = localized_event_datetime.astimezone(pytz.utc)
            timestamp = int(utc_event_datetime.timestamp())  # Convert to Unix timestamp

            # Check if event already exists
            event_ref = db.collection('events').document(str(timestamp))
            if event_ref.get().exists:
                return {"status": 422, "message": "Event already exists"}

            # Save event to Firestore
            event_ref.set({
                'timestamp': timestamp,
                'duration': event_duration
            })
            return {"status": 200, "message": "Event created successfully"}
        except Exception as e:
            return {"status": 500, "message": str(e)}

    @staticmethod
    def get_free_slots(date_str, target_timezone_str):
        """
        Get free slots for a given date in a specific timezone.
        """
        try:
            # Timezone information
            base_timezone = pytz.timezone(BASE_TIMEZONE)  # Base timezone for the slots
            target_timezone = pytz.timezone(target_timezone_str)  # Target timezone for the output
            utc_timezone = pytz.utc

            # Define the date range in base timezone
            date = datetime.strptime(date_str, '%Y-%m-%d')
            start_of_day_base = base_timezone.localize(datetime.combine(date, datetime.min.time()))
            end_of_day_base = base_timezone.localize(datetime.combine(date, datetime.max.time()))

            # Define the time range for slots in base timezone
            start_time_base = start_of_day_base.replace(hour=START_HOUR)  # Start time 10:00 AM
            end_time_base = start_of_day_base.replace(hour=END_HOUR)    # End time 05:00 PM

            # Convert start and end times to UTC epoch timestamps
            start_time_utc = start_time_base.astimezone(utc_timezone)
            end_time_utc = end_time_base.astimezone(utc_timezone)
            
            start_of_day_epoch = int(start_time_utc.timestamp())
            end_of_day_epoch = int(end_time_utc.timestamp())

            # Query events from Firestore using epoch timestamps
            events_query = db.collection('events') \
                .where('timestamp', '>=', start_of_day_epoch) \
                .where('timestamp', '<=', end_of_day_epoch) \
                .stream()

            events = [event.to_dict() for event in events_query]

            # Generate all slots in UTC epoch format
            all_slots = []
            current_time_utc = start_time_utc
            while current_time_utc <= end_time_utc:
                all_slots.append(int(current_time_utc.timestamp()))
                current_time_utc += timedelta(minutes=SLOT_DURATION_MINUTES)  # Slot interval

            # Filter out slots that overlap with existing events
            free_slots_utc = []
            for slot_epoch in all_slots:
                if not any(event['timestamp'] <= slot_epoch < event['timestamp'] + event['duration'] * 60 for event in events):
                    free_slots_utc.append(slot_epoch)

            # Convert free slots to the target timezone and format
            free_slots_target = []
            for slot_epoch in free_slots_utc:
                slot_time_utc = datetime.fromtimestamp(slot_epoch, tz=utc_timezone)
                slot_time_target = slot_time_utc.astimezone(target_timezone)
                free_slots_target.append(slot_time_target.strftime('%Y-%m-%dT%H:%M:%S%z'))

            return free_slots_target
        except Exception as e:
            return jsonify({"message": str(e), "status": 500}), 500

    @staticmethod
    def get_events(start_date_str, end_date_str, timezone_str=BASE_TIMEZONE):
        """
        Get all events between two dates, converting times from UTC to the specified timezone.
        """
        try:
            start_date = datetime.fromisoformat(start_date_str)
            end_date = datetime.fromisoformat(end_date_str)

            # Convert to UTC
            utc_timezone = pytz.utc
            start_date_utc = utc_timezone.localize(start_date)
            end_date_utc = utc_timezone.localize(end_date)

            # Query events from Firestore
            events_query = db.collection('events') \
                .where('timestamp', '>=', int(start_date_utc.timestamp())) \
                .where('timestamp', '<=', int(end_date_utc.timestamp())) \
                .stream()
                
            events = [event.to_dict() for event in events_query]

            # Convert event timestamps from UTC to the specified timezone
            local_timezone = pytz.timezone(timezone_str)
            for event in events:
                utc_datetime = datetime.fromtimestamp(event['timestamp'], pytz.utc)
                event['datetime'] = utc_datetime.astimezone(local_timezone).isoformat()

            return {"status": 200, "events": events}
        except Exception as e:
            return {"status": 500, "message": str(e)}
