import json
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from telegram_bot_1.models import Result

# Define the SQLAlchemy database engine and session
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()


# Read data from data.json file
with open('data.json') as json_file:
    data = json.load(json_file)

stepik_id = data["course-grades"][0]["id"]
course_id = data["course-grades"][0]["course"]
score = data["course-grades"][0]["score"]

model = Result(stepik_id=stepik_id, course_id=course_id, score=score)
session.add(model)

session.commit()
session.close()
