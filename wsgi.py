from core import create_app
from schema import AttendeeSchema
from models import *
from dotenv import load_dotenv
from dump import readCsv

import os

load_dotenv()

app = create_app(conf=os.getenv('APP_ENV'))


# util route
# # @app.get('/')
# # def dumpData():
# #     data = readCsv('result.csv')
# #     print(data)
# #     for r in data:
# #         schema = AttendeeSchema()
# #         attendee = schema.load(r)
# #         print(attendee)
#     #     db.session.add(attendee)
    
#     # try:
#     #     db.session.commit()
#     # except Exception as e:
#     #     print(str(e))
#     # finally:
#     #     db.session.close()
#     return {
#         'status': 'success'
#         # 'dta': attendee
    # }, 200

if __name__ == '__main__':
    app.run()
