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
    session_id = db.Column(db.Integer)


    @staticmethod
    def create_events():
        events = [
            "Introduction to GCP: A Guide to Google\'s Cloud-9",
            "Design and Motion: The Two Infinity Stones of Memorable User Experiences",
            "Transitioning from REST to GraphQL: Enhancing API Efficiency",
            "Web3 for Web2 Developers",
            "Unveiling the Power Within: Mastering Google Chrome DevTools for Web Excellence.",
            "Leveraging User psychology for Product Growth",
            "Turbocharge Your Angular Applications: The Power of Real-time with Angular Signals",
            "Navigating the Feasibility and Future Trends of Machine Learning Integration in Flutter Applications",
            "LangChain and LLMs: Building your own generation AI chatbot trained on your data with LangChain"
        ]

        for idx, event in enumerate(events):
            grp = idx//3 + 1
            new = Event(title=event, session_id=grp)
            db.session.add(new)
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(str(e))
            return 'failed'
        finally:
            db.session.close()
        
        return 'ok'
