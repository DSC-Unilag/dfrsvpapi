from extensions import ma, db
from marshmallow import fields
from models import Attendees


class Rsvp(ma.Schema):
    ticket_id = fields.String(required=True)
    event_ids = fields.List(
        fields.Integer(),
        required=True
    )

class checkRsvp(ma.Schema):
    ticket_id = fields.String(required=True)
    event_id = fields.Integer(required=True)


class AttendeeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Attendees
        load_instance = True
        sqla_session=db.session
