import requests  # Используется для отправки HTTP-запросов
from bs4 import BeautifulSoup  # Для парсинга HTML-контента
from shibzuko.config import CLIENT_ID, CLIENT_SECRET


def get_stepik_token():  # Используется для получения токена доступа к Stepik API
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    response = requests.post('https://stepik.org/oauth2/token/',  # Отправляет POST-запрос на URL с использованием базовой аутентификации (HTTPBasicAuth).
                            data={'grant_type': 'client_credentials'},
                            auth=auth)
    token = response.json().get('access_token', None)
    if not token:
        raise Exception('Unable to authorize with provided credentials')
    return token


def stepik_data(url, stepik_token):  # Получение данных из Stepik API
    response = requests.get(url,
                        headers={'Authorization': 'Bearer ' + stepik_token}) # отправляет GET-запрос на указанный URL с заголовком
    if response.status_code == 200:
        return response.json()
    else:
        stepik_token = get_stepik_token()
        return stepik_data(url, stepik_token)

url = 'https://stepik.org:443/api/users/315844473'

url2 = 'https://stepik.org/api/course-grades?course=68343&user=115507791'

stepik_token = get_stepik_token()
user = stepik_data(url2, stepik_token)

for k, v in user['course-grades'][0]['results'].items():
    print(k, v)
print(user['course-grades'][0]['results'])
print(user['course-grades'][0])
print(user['course-grades'])
print(user['course-grades'][0]['last_viewed']=='2023-06-10T23:54:31.428Z')
print(user['course-grades'][0]['score'])
# print(user['course-grades'][0]['results']['score'])

def html_title(url):  # Используется для получения заголовка HTML-страницы.
    # Send a GET request to the URL
    response = requests.get(url)  # Отправляет GET-запрос на указанный URL

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')  # Парсит HTML-контент

    # Extract the title
    title = soup.title.string.strip()[:-9]
    print(title)
    return title

# html_title('https://stepik.org/users/315844473')