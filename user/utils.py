from django.conf import settings
import requests
from rest_framework.exceptions import ValidationError


def createAuth0User(email,password,name):
    url = f'https://{settings.AUTH0_DOMAIN}/dbconnections/signup'
    payload = {
        'client_id': settings.AUTH0_CLIENT_ID,
        'email': email,
        'password': password,
        "name":name,
        'connection': 'Username-Password-Authentication'
    }
    response = requests.post(url, json=payload)
    # print("response",response.json())
    if response.status_code == 200:
        return response
    raise ValidationError(response.json())

def obtainTokenAuth0(email,password):
    url = f'https://{settings.AUTH0_DOMAIN}/oauth/token'
    payload = {
        'grant_type': 'password',
        'client_id': settings.AUTH0_CLIENT_ID,
        'client_secret': settings.AUTH0_CLIENT_SECRET,
        'username': email,
        'password': password,
        'scope': 'openid',
        'connection': 'Username-Password-Authentication'
    }
    response = requests.post(url, json=payload)
    return response