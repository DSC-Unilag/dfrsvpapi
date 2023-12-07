from flask import (
    Blueprint,
    request
)
from models import (
    Attendees,
    time_code,
    Event,
    Venue
)
from schema import EventSchema, VerifySchema

venue = Blueprint('venue', __name__, url_prefix='/venue')

@venue.get('/<venue_id>')
def fetch_venue_events(venue_id):
    events = Event.query.filter_by(venue_id=venue_id).all()
    schema = EventSchema(many=True)
    return {
        'status': 'success',
        'data': schema.dump(events)
    }

@venue.get('/time_codes')
def fetch_time_code():
    return {
        'status': 'success',
        'data': time_code
    }

@venue.post('/verify')
def verify():
    schema = VerifySchema()
    try:
        data = schema.load(request.get_json(force=True))
    except Exception as e:
        print(str(e))
        return {
            'msg':str(e),
            'status':'error'
        },400
    
    attendee_profile = Attendees.query.get(data['ticket_id'])
    if not attendee_profile:
        return {
            'status': 'error',
            'code': 10,
            'msg': f"Attendee with ticket_id {data['ticket_id']} not found"
        },404
    
    venue = Venue.query.get(data['venue_id'])
    if not venue:
        return {
            'status': 'error',
            'code': 11,
            'msg': f"venue with id {data['venue_id']} not found"
        }
    
    events = venue.events
    if not events:
        return {
            'status': 'error',
            'code': 12,
            'msg': f"Unverifiable ticket {data['ticket_id']}- please rsvp for sessions before hand"
        }
    curr = None
    for evnt in events:
        if time_code[data['time_code']] == evnt.session_id:
            curr = evnt
    
    if curr not in attendee_profile.events:
        return {
            'status': 'error',
            'code': 13,
            'msg': 'Attendee did not RSVP for this session'
        }, 400
    else:
        return {
            'status': 'success',
            'code': 20,
            'msg': 'Attendee verified for current session'
        }, 200