# Run with Python 3
import re

import requests
from config import CLIENT_ID, CLIENT_SECRET, COURSE_ID, STEPIK_ID, DEV_ID
from bs4 import BeautifulSoup

# 1. Get your keys at https://stepik.org/oauth2/applications/
# (client type = confidential, authorization grant type = client credentials)

# 2. Get a token
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
response = requests.post('https://stepik.org/oauth2/token/',
                         data={'grant_type': 'client_credentials'},
                         auth=auth)
token = response.json().get('access_token', None)
if not token:
    print('Unable to authorize with provided credentials')
    exit(1)

# 3. Get info about course
api_url = f'https://stepik.org/api/courses/{COURSE_ID}'
course = requests.get(api_url,
                      headers={'Authorization': 'Bearer ' + token}).json()

print(course)

# 4. Get course - grades
course_grades_url = f"https://stepik.org:443/api/course-grades?course={COURSE_ID}&user={STEPIK_ID}"
course_grades = course = requests.get(course_grades_url,
                                      headers={'Authorization': 'Bearer ' + token}).json()

print(course_grades)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from telegram_bot_1.models import Result, User

# Define the SQLAlchemy database engine and session
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()

stepik_id = course_grades["course-grades"][0]["id"]
course_id = course_grades["course-grades"][0]["course"]
score = course_grades["course-grades"][0]["score"]

model = Result(stepik_id=stepik_id, course_id=course_id, score=score)
session.add(model)

session.commit()
session.close()

# 4. PARSING user_name from stepik.org

parse_url = f"https://stepik.org/users/{STEPIK_ID}"
response = requests.get(parse_url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')
raw_name = soup.text
name_from_parse = soup.title.string.strip()[:-9]

print(name_from_parse)

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()

model = User(stepik_id=STEPIK_ID, tg_id=DEV_ID, name=name_from_parse)
session.add(model)

session.commit()
session.close()
