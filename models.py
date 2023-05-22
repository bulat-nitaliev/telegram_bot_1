from sqlite3 import Date

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Create an SQLite engine
engine = create_engine('sqlite:///database.db')

# Declare the "user" table model
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    stepik_id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    name = Column(String)

class Result(Base):
    __tablename__ = 'result'
    stepik_id = Column(Integer, primary_key=True)
    course_id = Column(Integer)
    score = Column(Integer)
    last_viewed = Column(Date)
    update_date = Column(Date)

# Create the table in the database
Base.metadata.create_all(engine)