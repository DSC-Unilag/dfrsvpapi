from flask import (
    Blueprint,
    request, 
    jsonify
)
from schema import (
    RsvpSchema,
    AttendeeSchema,
    checkRsvpSchema,
    EventSchema,
    EditRsvpSchema
)
from models import *

from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from flask_cors import cross_origin
from dump import readCsv


rsvp = Blueprint('rsvp', __name__, url_prefix='/rsvp')

# fetch rsvp sessions
@rsvp.get('/<ticket_id>')
def fetch_rsvps(ticket_id):
    attendee_profile: Attendees = Attendees.query.get(ticket_id)
    schema = EventSchema()
    if not attendee_profile:
        return {
            'status': 'error',
            'msg': f'Attendee with specified ticket id {ticket_id} not found'
        }, 404

    return {
        'status': 'success',
        'data': [schema.dump(event) for event in attendee_profile.fetchEvents()]
    }, 200


# rsvp for a session
@rsvp.post('/')
@cross_origin()
def sign_up():
    schema = RsvpSchema()
    try:
        data = schema.load(request.get_json(force=True))
    except Exception as e:
        print(str(e))
        return {
            'status': 'error',
            'msg': str(e)
        }
    
    attendee_profile: Attendees = Attendees.query.get(data['ticket_id'])
    if not attendee_profile:
        attendee_profile = Attendees(
            ticket_id=data['ticket_id'],
            first_name="late_comer"
        )
        db.session.add(attendee_profile)

    if attendee_profile.events.all():
        db.session.rollback()
        return {
            'status': 'error',
            'msg': f"It seems you already rspv'd"
        }, 409

    if len(attendee_profile.events.all()) == 4:
        db.session.rollback()
        return {
            'status': 'error',
            'msg': 'maximum number of events reached'
        }, 400
    
    sessions = set()

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
        if event.session_id in sessions:
            db.session.rollback()
            return {
                'status': 'error',
                'msg': 'cannot rsvp for more than one event in a session'
            }, 400
        sessions.add(event.session_id)
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


@rsvp.patch('/<ticket_no>')
def patch(ticket_no):
    # parse data
    schema = EditRsvpSchema()
    try:
        data = schema.load(request.get_json(force=True))
    except Exception as e:
        print(str(e))
        return {
            'status': 'error',
            'msg': str(e)
        }, 400
    
    # find attendee
    attendee_profile = Attendees.query.get(ticket_no)
    if not attendee_profile:
        return {
            'status': 'error',
            'msg': f'Attendee with id {ticket_no} not found'
        }, 404
    

    # edit rsvps
    rsvps = attendee_profile.events
    sessions = set([event.session_id for event in rsvps])

    for evnt in data['event_ids']:
        event = Event.query.get(evnt)
        if not event:
            return {
                'status': 'error',
                'msg': f"Event with specified id {evnt} not found"
            }, 404
        if event in rsvps:
            continue
        # redundant maybe, but shaa..
        try:
            if event.session_id in sessions:
                db.session.rollback()
                return {
                    'status': 'error',
                    'msg': 'cannot rsvp for more than one event in a session'
                }, 400
            attendee_profile.events.append(event)
            sessions.add(event.session_id)
        except IntegrityError as e:
            db.session.rollback()
            return {
                'status': 'error',
                'msg': f"It seems you already rspv'd for this event"
            }, 409
        except Exception as e:
            print(str(e))
            db.session.rollback()

    return {
        'status': 'success',
        'data': EventSchema(many=True).dump(attendee_profile.events)
    }


@rsvp.put('/<ticket_no>')
def put(ticket_no):
    schema = EditRsvpSchema()
    try:
        data = schema.load(request.get_json(force=True))
    except Exception as e:
        print(str(e))
        return {
            'status': 'error',
            'msg': str(e)
        }, 400
    
    # find attendee
    attendee_profile = Attendees.query.get(ticket_no)
    if not attendee_profile:
        return {
            'status': 'error',
            'msg': f'Attendee with id {ticket_no} not found'
        }, 404

    rsvps = attendee_profile.events
    sessions = set()
    replace = []

    for evnt in data['event_ids']:
        event = Event.query.get(evnt)
        if not event:
            return {
                'status': 'error',
                'msg': f"Event with specified id {evnt} not found"
            }, 404
        # redundant maybe, but shaa..
        try:
            if event.session_id in sessions:
                db.session.rollback()
                return {
                    'status': 'error',
                    'msg': 'cannot rsvp for more than one event in a session'
                }, 400
            replace.append(event)
            sessions.add(event.session_id)
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
        attendee_profile.events = replace
        resp = EventSchema(many=True).dump(attendee_profile.events)
        db.session.commit()
    except Exception as e:
        print(str(e))
    finally:
        db.session.close()
    
    return {
        'status': 'success',
        'data': resp
    }, 200

@rsvp.post('/verify')
@cross_origin()
def verify():
    schema = checkRsvpSchema()
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
