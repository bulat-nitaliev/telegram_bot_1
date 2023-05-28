# Run with Python 3
import requests

# 1. Get your keys at https://stepik.org/oauth2/applications/
# (client type = confidential, authorization grant type = client credentials)
client_id = "m9hLK9NrSQzAn6gu2Ngixpj9r690fnpoitivhoOC"
client_secret = "7mGzw1H3SOD1SdE0nB7cG5saNGuy2jM0xRq6hwN3yE9mXyO5ZPZVb08S06TKhGGjZ1GClDA77IXbUGKWcI76PDErf4zU1gIIK2djiAbNwoI8skOoIulOcdYyx6mqgRDT"

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
api_url = 'https://stepik.org:443/api/course-grades?course=100707&user=190715002'
course = requests.get(api_url,
                      headers={'Authorization': 'Bearer ' + token}).json()

print(course)