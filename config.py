import os
from dotenv import load_dotenv

load_dotenv('.env')
TOKEN = os.environ.get('TOKEN')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
STEPIK_ID = os.environ.get('STEPIK_ID')
COURSE_ID = os.environ.get('COURSE_ID')
