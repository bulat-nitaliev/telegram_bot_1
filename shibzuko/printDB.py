from shibzuko.models import Student, session


students = session.query(Student).all()

for student in students:
    print(f'student.id: {student.id},\n'
          f'student.name: {student.name},\n'
          f'student.tg_id: {student.tg_id},\n'
          f'student.tg_full_name: {student.tg_full_name},\n'
          f'student.tg_username: {student.tg_username},\n'
          f'student.results: {student.results}')

session.close()