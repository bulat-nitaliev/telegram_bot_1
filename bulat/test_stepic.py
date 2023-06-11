import json
import requests
from datetime import date
from stepic import get_stepik_token, stepik_data
from models import session, Student, Result, python_for_beginner, engine


stepic_token = get_stepik_token()
url = 'https://stepik.org:443/api/course-grades?course=58852&user=190715002'

data_for_beginer = stepik_data(url=url,stepik_token=stepic_token)
for_beginner = [i for i in data_for_beginer['course-grades'][0]['results']]
student_id = data_for_beginer['course-grades'][0]["user"]
course_id = data_for_beginer['course-grades'][0]["course"]
score = data_for_beginer['course-grades'][0]["score"]
current_time = date.today()
course_id = data_for_beginer['course-grades'][0]["course"]


obj = Result(
    student_id = student_id,
    course_id = course_id,
    score = score,
    update_date = current_time
)
session.add(obj)
session.commit()


# dic = data_for_beginer['course-grades'][0]['results']
# for name,result in sorted(dic.items()):
#     if result['is_passed']:
#         for i in sorted(for_beginner):
#             print(name,i)

#             with engine.connect() as conn:
#                 stmt = update(for_beginner).values(for_beginner.c.i=current_time)
#                 conn.execute(stmt)


