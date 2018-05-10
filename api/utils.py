import requests

def cURL_request(username, password):
    data = [
    ('grant_type', 'password'),
    ('username', username),
    ('password', password),
    ]

    response = requests.post('http://10.6.1.16:8000/o/token/', data=data, auth=('OoyFqtDsJS5Uomt4LSHTbYAhWOdGrwQ4VxdnFnej', '3PW6fMl5a5lCGLl9KLa75uA8FjGu6SESv723ojBYcqjSd3ZYHTxvwywT0w70196UfypbzqzOM0Qrq2VELUEldpzeepcyPpga9afRE9KitixVjcehtGNBlmizgu0cnP87'))
    return response