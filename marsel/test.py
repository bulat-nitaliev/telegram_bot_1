import json
from datetime import date, datetime, timedelta
from models import Result, Student, PythonForBeginner, session
from stepik import html_title, stepik_data, get_stepik_token
from static.data import beginner_columns

# # "Поколение Python": курс для начинающих
# PythonForBeginner_id = 58852
# # "Поколение Python": курс для продвинутых
# PythonForIntermediate_id = 68343
# # "Поколение Python": курс для профессионалов
# PythonForAdvanced_id = 82541


# stepik_id = 270531229
# url = f"https://stepik.org:443/api/course-grades?course={PythonForBeginner_id}&user={stepik_id}" 


# stepik_token = get_stepik_token()
# data = stepik_data(url=url, stepik_token=stepik_token)


with open('marsel/beginner_data.json', encoding='utf-8') as data:
    data = json.load(data)


student_id = data['course-grades'][0]["user"]
course_id = data['course-grades'][0]["course"]
last_viewed = datetime.strptime(
    data['course-grades'][0]["last_viewed"][:10], 
    '%Y-%m-%d'
    ).date()

current_time = date.today()

delta = current_time - last_viewed
if delta <= timedelta(days=7):
    steps_data = {"student_id": student_id, "update_date": current_time}
    row = session.query(PythonForBeginner).filter_by(student_id=student_id).first()
    if row:
        not_passed_steps = [key for key, value in row.__dict__.items() if not value]    
    else:
        not_passed_steps = beginner_columns
    for step, status in data['course-grades'][0]["results"].items():
        if status['is_passed']:
            if step in not_passed_steps:
                steps_data[step] = current_time
    obj = PythonForBeginner(**steps_data)
    session.merge(obj)
    session.commit()
else:
    pass


    











# obj = session.query(PythonForBeginner).filter_by(student_id=stepik_id).first()
# for column in PythonForBeginner.__table__.columns:
#     filtered_objects = session.query(PythonForBeginner).filter(getattr(PythonForBeginner, column.name).isnot(None))
#     # ==None
#     print(column.name)




# print(stepik_id, current_time)

# obj = PythonForBeginner(
#     student_id=stepik_id,
#     update_date=current_time,
#     c265077_4=current_time
# )
# session.merge(obj)
# session.commit()

# obj = session.query(PythonForBeginner).filter_by(student_id=stepik_id).first()
# student_id = data['course-grades'][0]["user"]
# course_id = data['course-grades'][0]["course"]
# score = data['course-grades'][0]["score"]
# current_time = date.today()

# obj = Result(
#     student_id = student_id,
#     course_id = course_id,
#     score = score,
#     update_date = current_time
# )
# session.add(obj)
# session.commit()

# my_stepik_id = 270531229
# url = f"https://stepik.org/users/{my_stepik_id}"
# name = html_title(url)

# obj = Student(
#     id = my_stepik_id,
#     name = name
# )
# session.add(obj)
# session.commit()
