from flask import Blueprint, request, jsonify
from schema import Rsvp, AttendeeSchema, checkRsvp
from models import *

from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from flask_cors import cross_origin
from dump import readCsv


rsvp = Blueprint('rsvp', __name__, url_prefix='/rsvp')

# fetch rsvp sessions
@rsvp.get('/<ticket_id>')
@cross_origin()
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
@cross_origin()
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

    if attendee_profile.events.all():
        db.session.rollback()
        return {
            'status': 'error',
            'msg': f"It seems you already rspv'd"
        }, 409

    for evnt in data['event_ids']:
        event = Event.query.get(evnt)
        if not event:
            return {
                'status': 'error',
                'msg': f"Event with specified id {evnt} not found"
            }, 404
        if event in attendee_profile.events:
            db.session.rollback()
            return {
                'status': 'error',
                'msg': f"It seems you already rspv'd for this event"
            }, 409
        try:
            attendee_profile.events.append(event)
        except IntegrityError as e:
            db.session.rollback()
            return {
                'status': 'error',
                'msg': f"It seems you already rspv'd for this event"
            }, 409
        except Exception as e:
            print(str(e))
            db.session.rollback()

    try:
        db.session.commit()
        resp = attendee_profile.fetchEvents()
    except Exception as e:
        db.session.rollback
    finally:
        db.session.close()
    return  {
        'status': 'success',
        'data': [{"id": event.id, "title": event.title} for event in resp]
    }, 202


@rsvp.post('/verify')
@cross_origin()
def verify():
    schema = checkRsvp()
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


@rsvp.get('/dump')
@cross_origin()
def dumpData():
    data = readCsv('result.csv')
    print(data[0])
    schema = AttendeeSchema()
    for r in data:
        attendee = schema.load(data[0])
        db.session.add(attendee)
    
    try:
        db.session.commit()
    except Exception as e:
        print(str(e))
        db.session.rollback()
    finally:
        db.session.close()

    return 'ok', 200


@rsvp.get('/events')
@cross_origin()
def fetch_events():
    events = Event.query.all()
    resp = [{
        'title':evnt.title, 
        'id':evnt.id,
        'speaker':evnt.speaker,
        'time': evnt.time,
        'session_id':evnt.session_id
        } for evnt in events]
    return {
        'status': 'success',
        'data': resp
    }
