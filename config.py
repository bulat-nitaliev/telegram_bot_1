import os
from dotenv import load_dotenv

load_dotenv('.env')

TOKEN = os.environ.get('TOKEN')
DEV_ID = os.environ.get("DEV_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
BOT_NAME = os.environ.get("BOT_NAME")
GROUP_ID = os.environ.get("GROUP_ID")
tg_bot = os.environ.get("tg_bot")
tg_grupp = os.environ.get("tg_grupp")
