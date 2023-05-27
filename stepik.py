import requests
from bs4 import BeautifulSoup
from config import CLIENT_ID, CLIENT_SECRET

url = "https://stepik.org/users/270531229"
url = "https://stepik.org/lesson/265077/step/4"
url = "https://stepik.org:443/api/course-grades?course=68343&user=270531229" 
headers = {"Authorization": "Bearer H1mo6LfJ6hjpepmAcsOPiJGnb8Ddg7"}


auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
response = requests.post('https://stepik.org/oauth2/token/',
                         data={'grant_type': 'client_credentials'},
                         auth=auth)
token = response.json().get('access_token', None)
if not token:
    print('Unable to authorize with provided credentials')
    exit(1)

api_url = 'https://stepik.org/api/courses/67'
course = requests.get(api_url,
                      headers={'Authorization': 'Bearer ' + token}).json()

print(course)



def html_title(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the title
    title = soup.title.string.strip()[:-9]

    return title