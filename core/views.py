from flask import Blueprint, request
from schema import Rsvp
from models import *

from psycopg2.errors import UniqueViolation


rsvp = Blueprint('rsvp', __name__, url_prefix='/rsvp')

# fetch rsvp sessions
@rsvp.get('/<ticket_id>')
def fetch_rsvps(ticket_id):
    attendee_profile: Attendees = Attendees.query.get(ticket_id)
    if not attendee_profile:
        return {
            'status': 'error',
            'msg': f'Attendee with specified ticket id {ticket_id} not found'
        }, 404

    return {
        'status': 'success',
        'data': [event.title for event in attendee_profile.fetchEvents()]
    }, 200


# rsvp for a session
@rsvp.post('/')
def sign_up():
    schema = Rsvp()
    try:
        data = schema.load(request.get_json(force=True))
    except Exception as e:
        print(str(e))
        return {
            'status': 'error',
            'msg': schema.error_messages
        }
    
    attendee_profile: Attendees = Attendees.query.get(data['ticket_id'])
    if not attendee_profile:
        return {
            'status': 'error',
            'msg': f"Attendee with specified ticket id {data['ticket_id']} not found"
        }, 404

    event = Event.query.get(data['event_id'])
    if not event:
        return {
            'status': 'error',
            'msg': f"Event with specified id {data['event_id']} not found"
        }, 404

    try:
        attendee_profile.events.append(event)
        db.session.commit()
    except UniqueViolation as e:
        db.session.rollback()
        return {
            'status': 'error',
            'msg': f"It seems you already rspv'd for this event"
        }, 409
    except Exception as e:
        print(str(e))
        db.session.rollback()
    finally:
        db.session.close()
    
    return  {
        'status': 'success',
        # 'data': [event.title for event in attendee_profile.fetchEvents()]
    }, 202


@rsvp.post('/verify')
def verify():
    schema = Rsvp()
    try:
        data = schema.load(request.get_json(force=True))
    except Exception as e:
        print(str(e))
        return {
            'status': 'error',
            'msg': schema.error_messages
        }
    
    attendee_profile: Attendees = Attendees.query.get(data['ticket_id'])
    if not attendee_profile:
        return {
            'status': 'error',
            'msg': f"Attendee with specified ticket id {data['ticket_id']} not found"
        }, 404

    event = Event.query.get(data['event_id'])
    if not event:
        return {
            'status': 'error',
            'msg': f"Event with specified id {data['event_id']} not found"
        }, 404
    
    # fetch all attendees for event.fi
    attendee = event.attendees.filter_by(ticket_id=attendee_profile.ticket_id).first()

    if not attendee:
        resp = False
    else:
        resp = True

    return {
        'status': 'success',
        'is_attending': resp
    }, 200
