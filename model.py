from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///your_database.db', echo=True)

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
	score = Column(Float)
	last_viewed = Column(Date)
	update_date = Column(Date)
	
Base.metadata.create_all(engine)