import requests

def cURL_request(username, password):
    data = [
    ('grant_type', 'password'),
    ('username', username),
    ('password', password),
    ]

    response = requests.post('http://localhost:8000/o/token/', data=data, auth=('NwVaE1ddbUDyzlCf0MvdVy7fRbwGCskjXtMPJy0z', '5zpukHVfn8vllOCaROBTXFt9MCK49Lbn6PbGjpFqNGAY5ajB9jii18vILtnEDE6sdLlrJ3gGQztb14Dee589JKOMTXgULON1vfxfPsAeOkaxPBuTPNWQCG8NsQhiO0vN'))
    return response