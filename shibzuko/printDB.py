from shibzuko.models import Student, Result, Table, session

results = session.query(Result).all()
students = session.query(Student).all()


for student in students:
    print(f'student.id: {student.id},\n'
          f'student.name: {student.name},\n'
          f'student.tg_id: {student.tg_id},\n'
          f'student.tg_full_name: {student.tg_full_name},\n'
          f'student.tg_username: {student.tg_username},\n'
          f'student.results: {student.results}')
print('=========\n\n\n\n')

for result in results:
      print(f'result.student_id: {result.student_id}')

session.close()