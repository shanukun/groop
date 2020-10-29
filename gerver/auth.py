from .models import Profile
from groop.settings import SECRET_KEY as secret
import jwt
import time


def encode(profile):
    username = profile['user']['username']

    return {
        'access': jwt.encode({'username': username, 'exp': int(time.time()) + 15 * 60 },
                             secret,
                             algorithm='HS256'),
        'refresh': jwt.encode({'username': username, 'exp': int(time.time()) + 48 * 3600 },
                              secret,
                              algorithm='HS256')
    }


def decode(token):
    payload = jwt.decode(token, secret, algorithms=['HS256'])
    return payload
