import requests

url = 'http://localhost:5000/login'

data = {
    'username': 'myusername',
    'password': 'mypassword'
}

response = requests.post(url, json=data)

print(response.json())
