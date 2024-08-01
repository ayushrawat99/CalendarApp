
This project is a backend service for an appointment booking system, designed to streamline scheduling. It uses Flask and Firestore to provide APIs for event management, including creating events, fetching free slots, and retrieving events.

## Features
- **Event Creation:** Create events with specific dates and durations.
- **Free Slot Retrieval:** Fetch available time slots for booking.
- **Event Retrieval:** Get events within a specified date range.

## Installation

### Prerequisites
- Python 3.x

### Steps
1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd <repository_directory>
Create and activate a virtual environment:


### Create a virtual environment and activate it:

bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install the dependencies:

bash
pip install -r requirements.txt


### API Endpoints


1. Ping
Endpoint: /ping
Method: GET
Description: Health check purpose.
Response: { "response": "pong" }



2. Create Event
Endpoint: /create-event
Method: POST
Description: Create a new event. 

Body - {
  "datetime": "2024-11-01T15:30:00",
  "duration": 45
}

Response - {
  "status": 200,
  "message": "Event created successfully"
}


3.  Get Free Slots
Endpoint: /free-slots
Method: GET
Description: Get available time slots for a given date and timezone.
Parameters:
date: The date for which to find free slots (format: YYYY-MM-DD).
timezone  The desired timezone for the free slots.

Response - 
 [
"2024-11-01T12:00:00+1100",
"2024-11-01T12:30:00+1100",
"2024-11-01T13:00:00+1100",
"2024-11-01T13:30:00+1100",
"2024-11-01T14:00:00+1100",
"2024-11-01T14:30:00+1100",
"2024-11-01T15:00:00+1100",
"2024-11-01T15:30:00+1100",
"2024-11-01T16:00:00+1100",
"2024-11-01T16:30:00+1100",
"2024-11-01T17:00:00+1100",
"2024-11-01T18:30:00+1100",
"2024-11-01T19:00:00+1100"
] 

4.  Get Events
Endpoint: /get-events
Method: GET
Description: Get all events between specified start and end dates.
Parameters:
start_date (required): The start date (format: YYYY-MM-DDTHH:MM:SS).
end_date (required): The end date (format: YYYY-MM-DDTHH:MM:SS).
Response: {
    "events": [
{
"datetime": "2024-11-01T15:30:00+09:00",
"duration": 45,
"timestamp": 1730442600
}
],
    "status": 200
}
