import os

from dotenv import load_dotenv

load_dotenv('.env')
TOKEN = os.environ.get('TOKEN')