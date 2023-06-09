# Run with Python 3
import requests
import json
from config import client_id, client_secret,stepik_id,course_id
# 1. Get your keys at https://stepik.org/oauth2/applications/
# (client type = confidential, authorization grant type = client credentials)
client_id = client_id
client_secret = client_secret

# 2. Get a token
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
response = requests.post('https://stepik.org/oauth2/token/',
                         data={'grant_type': 'client_credentials'},
                         auth=auth)
token = response.json().get('access_token', None)
if not token:
    print('Unable to authorize with provided credentials')
    exit(1)

# 3. Call API (https://stepik.org/api/docs/) using this token.
api_url = f'https://stepik.org:443/api/course-grades?course={course_id}&user={stepik_id}'
course = requests.get(api_url,
                      headers={'Authorization': 'Bearer ' + token}).json()

api_url = f'https://stepik.org:443/api/users/{stepik_id}'
name = requests.get(api_url,
                      headers={'Authorization': 'Bearer ' + token}).json()

s1 = json.dumps(course)
s2 = json.dumps(name)
data = json.loads(s1)
stepic_name = json.loads(s2)['users'][0]['full_name']
