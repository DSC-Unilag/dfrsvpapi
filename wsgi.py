from core import create_app
from models import *
from dotenv import load_dotenv


import os

load_dotenv()

app = create_app(conf=os.getenv('APP_ENV'))


if __name__ == '__main__':
    app.run()
