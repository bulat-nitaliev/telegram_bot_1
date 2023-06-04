import requests
import config
from bot.py import stepik_id, tg_id
from models import Student, session
from datetime import datetime
import json

def get_token():
    auth = requests.auth.HTTPBasicAuth(config.CLIENT_ID, config.CLIENT_SECRET)
    resp = requests.post('https://stepik.org/oauth2/token/',
                         data={'grant_type': 'client_credentials'},
                         auth=auth)
    return resp.json()['access_token']

def get_user_data():
    token = get_token()
    response = requests.get(
        f'https://stepik.org:443/api/users/{stepik_id}',
        headers={'Authorization': 'Bearer ' + token}
    )
    return response.json()


data = get_data()
# Создаем объект Student с данными из JSON
result = Student(
    stepik_id=data["users"][0].get("full_name"),
    course_id=data["course-grades"][0].get('course'),
    score=data["course-grades"][0].get('score'),
    last_viewed=datetime.strptime(data["course-grades"][0].get('last_viewed'), '%Y-%m-%dT%H:%M:%S.%fZ').date(),
    
    # update_date=data["course-grades"][0].get('update_date')

    id = stepik_id
    name = data["users"][0].get("full_name")
    tg_id = tg_id
    tg_full_name = Column(String)
    tg_username = Column(String)
)

# Добавляем объект Result в сессию
session.add(result)

# Фиксируем изменения в базе данных
session.commit()

# Закрываем сессию
session.close()
user = message.from_user
first_name = user.first_name  # Имя пользователя
last_name = user.last_name    # Фамилия пользователя (может быть None)
username = user.username      # Юзернейм пользователя (может быть None)
if last_name:
    full_name = f"{first_name} {last_name}"
else:
    full_name = first_name