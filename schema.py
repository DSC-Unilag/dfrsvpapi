from extensions import ma, db
from marshmallow import (
    fields,
    validate
)
from models import Attendees


class Rsvp(ma.Schema):
    ticket_id = fields.String(required=True, validate=validate.Regexp("^DSCA[0-9]{9}$"))
    event_ids = fields.List(
        fields.Integer(),
        required=True,
        validate=validate.Length(max=3)
    )

class checkRsvp(ma.Schema):
    ticket_id = fields.String(required=True, validate=validate.Regexp("^DSCA[0-9]{9}$"))
    event_id = fields.Integer(required=True)


class AttendeeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Attendees
        load_instance = True
        sqla_session=db.session
