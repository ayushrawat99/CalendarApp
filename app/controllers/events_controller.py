from flask import Blueprint, request, jsonify
from app.services.events_service import EventsService

# Define a Blueprint for events
events_bp = Blueprint('events_bp', __name__)

# Endpoint to create an event
@events_bp.route('/create-event', methods=['POST'])
def create_event():
    data = request.json
    response = EventsService.create_event(data)
    return jsonify(response), response["status"]

# Endpoint to get free slots
@events_bp.route('/free-slots', methods=['GET'])
def get_free_slots():
    date = request.args.get('date')
    timezone = request.args.get('timezone', 'UTC')
    free_slots = EventsService.get_free_slots(date,timezone)
    return jsonify(free_slots), 200

# Endpoint to get events
@events_bp.route('/get-events', methods=['GET'])
def get_events():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    response = EventsService.get_events(start_date, end_date)
    return response
