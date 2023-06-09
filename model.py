import sqlalchemy as db
from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
engine = create_engine('sqlite:///your_database.db', echo=True)


Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	tg_id = Column(Integer)
	tg_fullname = (String)
	stepik_id = Column(Integer)
	course_id = Column(Integer)
	results = relationship("Result", backref='author' )

class Result(Base):
	__tablename__ = 'result'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	score = Column(Float)
	last_viewed = Column(Date)
	user_id = Column(Integer, db.ForeignKey('user.id'), nullable=False)


Base.metadata.create_all(engine)