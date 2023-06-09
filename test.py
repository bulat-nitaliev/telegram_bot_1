import json
from datetime import date
from sqlalchemy.orm.session import sessionmaker
from model import engine, User, Result
from stepic_api import  data, stepic_name
from config import stepik_id, course_id, tg_fullname, DEV_ID


session = sessionmaker(bind=engine)()
#User
tg_id = DEV_ID
tg_fullname = tg_fullname
stepik_id = stepik_id
course_id = course_id

new_user = User(tg_id=tg_id,tg_fullname=tg_fullname,stepik_id=stepik_id,course_id=course_id)

session.add(new_user)
session.commit()


user = session.query(User).filter(User.id==1).first()

#Result
name = stepic_name
score = data['course-grades'][0]['score']
y,m,d = map(int,data['course-grades'][0]['last_viewed'][:10].split('-'))
last_viewed = date(y,m,d)

result = Result(name=stepic_name,score=score,last_viewed=last_viewed,author=user)


session.add(result)
session.commit()
