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
    speaker = db.Column(db.String())
    speaker_bio = db.Column(db.Text)
    time = db.Column(db.String)


    @staticmethod
    def create_events():
        events = [
            {
                "title": "Introduction to GCP: A Guide to Google\'s Cloud-9",
                "speaker": "Oluwagbemileke Kolawole - Cloud Enginner",
                "time": ""
            },
            {
                "title": "Design and Motion: The Two Infinity Stones of Memorable User Experiences",
                "speaker": "Chinaza Icheke- UI/UX Designer"
            },
            {
               "title": "Transitioning from REST to GraphQL: Enhancing API Efficiency",
               "speaker": "Adejoke Haastrup-Software Engineer"
            },
            {
                "title": "Web3 for Web2 Developers",
                "speaker": "Idris Olubisi- Developer Advocate, Axelar"
            },
            {
                "title": "Unveiling the Power Within: Mastering Google Chrome DevTools for Web Excellence.",
                "speaker": "Jesus Akanle - Content Lead (GDSC Unilag)"
            },
            {
                "title": "Leveraging User psychology for Product Growth",
                "speaker": "TGoodness Ehizode- Product Leader"
            },
            {
                "title": "Turbocharge Your Angular Applications: The Power of Real-time with Angular Signals",
                "speaker": "Olayinka Atobiloye-GitHub Campus Expert"
            },
            {
                "title": "Navigating the Feasibility and Future Trends of Machine Learning Integration in Flutter Applications",
                "speaker": "Ogbonna Emmanuella-Flutter Developer"
            },
            {
                "title": "LangChain and LLMs: Building your own generation AI chatbot trained on your data with LangChain",
                "speaker": "Salim Oyinlola- Gold Microsoft Ambassador"
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
