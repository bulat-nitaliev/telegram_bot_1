import os

from dotenv import load_dotenv

load_dotenv('.env')
TOKEN = os.environ.get('TOKEN')
DEV_ID = os.environ.get("DEV_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
CHAT_ID = os.environ.get('CHAT_ID')