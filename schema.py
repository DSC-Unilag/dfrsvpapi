from extensions import ma
from marshmallow import fields


class Rsvp(ma.Schema):
    ticket_id = fields.String(required=True)
    event_id = fields.Integer(required=True)
