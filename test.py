import json
from datetime import date
from sqlalchemy.orm.session import sessionmaker
from model import engine, User, Result



session = sessionmaker(bind=engine)()

with open(r'C:\Users\6417\Desktop\Bot\telegram_bot_1\data.json',encoding='utf-8') as file, open(r'C:\Users\6417\Desktop\Bot\telegram_bot_1\test.txt','w',encoding='utf-8') as test:
	data, dic = json.load(file), {}
	for i,j in data.items():
		if i == 'course-grades':
			for x in j:
				for key, value in x.items():
					if key == 'id':
						dic['stepik_id'] = value
					if key == 'course':
						dic['course_id'] = value
					if key == 'score':
						dic['score'] = value
					if key == 'last_viewed':
						y,m,d = map(int,value[:10].split('-'))
						dic['last_viewed'] = date(y,m,d)
					if key == 'certificate_update_date':
						y,m,d = map(int,value[:10].split('-'))
						dic['update_date'] = date(y,m,d)
	#json.dump(dic,test)

result = Result(stepik_id=dic['stepik_id'],course_id=dic['course_id'],score=dic['score'],last_viewed=dic['last_viewed'],update_date=dic['update_date'])
session.add(result)
session.commit()
