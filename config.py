import os

from dotenv import load_dotenv

load_dotenv('.env')
TOKEN = os.environ.get('TOKEN')
DEV_ID = os.environ.get('DEV_ID')
client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
stepik_id = os.environ.get('stepik_id')
course_id = os.environ.get('course_id')
tg_fullname = os.environ.get('tg_fullname')