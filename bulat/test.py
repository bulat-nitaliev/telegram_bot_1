import json
from datetime import date
from models import Result, Student, session
from stepic import stepik_data


with open('data.json', encoding='utf-8') as data:
    data = json.load(data)

student_id = data['course-grades'][0]["user"]
course_id = data['course-grades'][0]["course"]
score = data['course-grades'][0]["score"]
current_time = date.today()

obj = Result(
    student_id = student_id,
    course_id = course_id,
    score = score,
    update_date = current_time
)
session.add(obj)
session.commit()

# my_stepik_id = 270531229
# url = f"https://stepik.org/users/{my_stepik_id}"
# #name = html_title(url)
# stepik_token = get_stepik_token()
# user_data = stepik_data(url, stepik_token)
# name = user_data['users'][0]['full_name']

# obj = Student(
#     id = my_stepik_id,
#     name = name
# )
# session.add(obj)
# session.commit()