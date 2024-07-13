from django.contrib.auth import authenticate
import requests
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

def get_username(username):
    username = username.replace('|', '.')
    return username

def jwt_get_username_from_payload_handler(payload,token,*args,**kwargs):
    username = get_username(payload.get('sub'))
    try:
        # if user is created using our api
        User.objects.get(username=username)
    except:
        # if user is created on auth0 but don't exists on our api
        url = settings.JWT_ISSUER + 'userinfo'
        response = requests.get(url,headers={"Authorization":"Bearer "+token})
        data = response.json()
        username = get_username(data['sub'])
        email = data['email']
        name = data['name']
        user = User(username=username,email=email,name=name)
        user.save()
    return username

import json
import jwt

def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get('https://{}/.well-known/jwks.json'.format(settings.AUTH0_DOMAIN)).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = 'https://{}/'.format(settings.AUTH0_DOMAIN)
    return jwt.decode(token, public_key, audience=settings.API_IDENTIFIER, issuer=issuer, algorithms=['RS256'])