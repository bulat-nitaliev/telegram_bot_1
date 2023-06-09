import json
from datetime import date
from .models import Result, Student, session, python_for_beginner, engine, Base
from .stepik import stepik_data, get_stepik_token
from sqlalchemy import update, insert
from datetime import datetime



with open('data.json', encoding='utf-8') as data:
    data = json.load(data)

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
course_id = '58852'
stepik_id = ''
stepik_token = get_stepik_token()

# Получение всех записей из модели Student
students = session.query(Student).all()

# Обход результатов
for student in students:
    student_id = student.id
    user_data_url = f"https://stepik.org:443/api/course-grades?course={course_id}&user={student_id}"
    #Данные со stepik через API
    user_data = stepik_data(user_data_url, stepik_token)
    #Данные из файла data.json
    #user_data = data
    last_viewed = datetime.strptime(user_data['course-grades'][0]["last_viewed"], "%Y-%m-%dT%H:%M:%SZ").date()
    date_today = date.today()
    delta = last_viewed - date_today
    if delta.days <= 1:
        begin_obj = session.query(python_for_beginner).filter_by(student_id=student_id).first()
        if not begin_obj:
            insert_query = python_for_beginner.insert().values(student_id=student_id, update_date=date.today())
            session.execute(insert_query)
            session.commit()
            for key, item in user_data['course-grades'][0]["results"].items():
                if user_data['course-grades'][0]["results"][key]["is_passed"]:
                    update_query = update(python_for_beginner).values(**{key: date.today()})
                    session.execute(update_query)
                    session.commit()
        else:
            for key, item in user_data['course-grades'][0]["results"].items():
                if not getattr(begin_obj, key) and user_data['course-grades'][0]["results"][key]["is_passed"]:
                    update_query = update(python_for_beginner).where(python_for_beginner.c.student_id == student_id).values(**{key: date.today()}, update_date=date.today())
                    # Выполняем запрос обновления
                    session.execute(update_query)
                    session.commit()



score = user_data['course-grades'][0]["score"]
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
# name = html_title(url)

# obj = Student(
#     id = my_stepik_id,
#     name = name
# )
# session.add(obj)
# session.commit()
