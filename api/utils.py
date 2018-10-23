import requests

def cURL_request(username, password):
    data = [
    ('grant_type', 'password'),
    ('username', username),
    ('password', password),
    ]

    response = requests.post('http://localhost:8000/o/token/', data=data, auth=('', ''))
    return response