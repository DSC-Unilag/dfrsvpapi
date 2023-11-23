from extensions import db
import sqlalchemy as sa


registrations = db.Table(
    'registrations',
    sa.Column(
        'ticket_id',
        sa.String(),
        sa.ForeignKey('attendees.ticket_id'),
        primary_key=True
    ),
    sa.Column(
        'event_id',
        sa.Integer(),
        sa.ForeignKey('event.id'),
        primary_key=True
    )
)


class Attendees(db.Model):
    id = db.Column(db.Integer)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    ticket_id = db.Column(db.String(), primary_key=True)
    events = db.relationship(
        'Event',
        secondary=registrations,
        backref=db.backref('attendees', lazy='dynamic'),
        lazy='dynamic'
    )

    def fetchEvents(self):
        return self.events.all()


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
