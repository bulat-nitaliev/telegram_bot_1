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

my_stepik_id = 56576756
url = f"https://stepik.org/users/{my_stepik_id}"
name = html_title(url)

obj = Student(        
    name = name
)
session.add(obj)
session.commit()

