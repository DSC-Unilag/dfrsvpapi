from extensions import ma, db
from marshmallow import (
    fields,
    validate
)
from models import Attendees, Event


class RsvpSchema(ma.Schema):
    ticket_id = fields.String(required=True, validate=validate.Regexp("^DSCA[0-9]{9}$"))
    event_ids = fields.List(
        fields.Integer(),
        required=True,
        validate=validate.Length(max=4)
    )

class EditRsvpSchema(ma.Schema):
    event_ids = fields.List(
        fields.Integer(),
        required=True,
        validate=validate.Length(max=4)
    )

class checkRsvpSchema(ma.Schema):
    ticket_id = fields.String(required=True, validate=validate.Regexp("^DSCA[0-9]{9}$"))
    event_id = fields.Integer(required=True)


class AttendeeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Attendees
        load_instance = True
        sqla_session=db.session


class EventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Event
        load_instance = True


class VerifySchema(ma.Schema):
    ticket_id = fields.String(required=True, validate=validate.Regexp("^DSCA[0-9]{9}$"))
    venue_id = fields.String(required=True, validate=validate.Length(max=10))
    time_code = fields.String(required=True, validate=validate.OneOf([
        "MYWKLBUP", "QILRK0Q5", "ECW0C6W3", "QRAQWC42"
    ]))
    