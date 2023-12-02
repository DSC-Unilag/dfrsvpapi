from extensions import db
import sqlalchemy as sa
import random


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

def generate_token(length, special_chars=False, upper_case_only=True):
    chars = "abcdefghijkmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ0123456789"

    if special_chars:
        chars += "~!@#$%^&*()?+_-[]{};><"

    token = "".join(random.choice(chars) for x in range(length))

    if upper_case_only:
        token = token.upper()

    return token


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
    speaker = db.Column(db.String())
    speaker_bio = db.Column(db.Text)
    time = db.Column(db.String)
    venue_id = db.Column(db.String(), db.ForeignKey('venue.venue_id'))


    @staticmethod
    def create_events():
        events = [
            {
                "title": "Introduction to GCP: A Guide to Google\'s Cloud-9",
                "speaker": "Oluwagbemileke Kolawole - Cloud Enginner",
                "venue_id": "5VY1UVM83P"
            },
            {
                "title": "Design and Motion: The Two Infinity Stones of Memorable User Experiences",
                "speaker": "Chinaza Icheke - UI/UX Designer",
                "venue_id": "JUZGQ3JWAY"
            },
            {
               "title": "Transitioning from REST to GraphQL: Enhancing API Efficiency",
               "speaker": "Adejoke Haastrup - Software Engineer",
               "venue_id": "3XJXRHFH6D"
            },
            {
                "title": "Web3 for Web2 Developers",
                "speaker": "Idris Olubisi - Developer Advocate, Axelar",
                "venue_id": "5VY1UVM83P"
            },
            {
                "title": "Unveiling the Power Within: Mastering Google Chrome DevTools for Web Excellence.",
                "speaker": "Jesus Akanle - Content Lead (GDSC Unilag)",
                "venue_id": "JUZGQ3JWAY"
            },
            {
                "title": "Leveraging User psychology for Product Growth",
                "speaker": "TGoodness Ehizode - Product Leader",
                "venue_id": "3XJXRHFH6D"
            },
            {
                "title": "Turbocharge Your Angular Applications: The Power of Real-time with Angular Signals",
                "speaker": "Olayinka Atobiloye - GitHub Campus Expert",
                "venue_id": "5VY1UVM83P"
            },
            {
                "title": "Navigating the Feasibility and Future Trends of Machine Learning Integration in Flutter Applications",
                "speaker": "Ogbonna Emmanuella - Flutter Developer",
                "venue_id": "JUZGQ3JWAY"
            },
            {
                "title": "LangChain and LLMs: Building your own generation AI chatbot trained on your data with LangChain",
                "speaker": "Salim Oyinlola - Gold Microsoft Ambassador",
                "venue_id": "3XJXRHFH6D"
            }
        ]

        for idx, event in enumerate(events):
            grp = idx//3 + 1
            time_mp = {
                1: "10.00AM - 10.40AM",
                2: "10:45AM - 11:35AM",
                3: "11:30PM - 12:10PM"
            }
            new = Event(
                title=event['title'],
                session_id=grp,
                speaker=event['speaker'],
                venue_id=event['venue_id'],
                time=time_mp[grp]
            )
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


class Venue(db.Model):
    venue_id = db.Column(db.String(10), primary_key=True)
    events = db.relationship('Event', backref='venue')

    @staticmethod
    def create_venues():
        ids = [
            generate_token(
                length=10,
                upper_case_only=True
            ) for _ in range(3)
        ]
        for tk in ids:
            new_venue = Venue(venue_id=tk)
            db.session.add(new_venue)
        try:
            db.session.commit()
        except Exception as e:
            print(str(e))
            return 'not ok'
        finally:
            db.session.close()

        return 'ok'
