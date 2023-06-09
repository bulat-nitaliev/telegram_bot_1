import os

from dotenv import load_dotenv

load_dotenv('.env')
TOKEN = os.environ.get('TOKEN')
<<<<<<< HEAD
DEV_ID = os.environ.get('DEV_ID')
client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
stepik_id = os.environ.get('stepik_id')
course_id = os.environ.get('course_id')
tg_fullname = os.environ.get('tg_fullname')
=======
DEV_ID = os.environ.get("DEV_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
GROUP_ID = os.environ.get("GROUP_ID")
BOT_NAME = os.environ.get("BOT_NAME")
>>>>>>> main
