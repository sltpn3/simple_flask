from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate
from jose import jwt
from time import time
from google.oauth2 import id_token
from google.auth.transport import requests


import requests

GOOGLE_PUBLIC_KEY_URL = "https://www.googleapis.com/oauth2/v3/certs"
GOOGLE_PUBLIC_KEYS = {}
LAST_KEY_FETCH = 0
KEY_CACHE_EXP = 60*60*6  # get new key every 6 hours

def _fetch_public_keys():
    # Check to see if the public key is unset or is stale before returning
    global LAST_KEY_FETCH
    global GOOGLE_PUBLIC_KEYS

    if (LAST_KEY_FETCH + KEY_CACHE_EXP) < int(time())\
            or not GOOGLE_PUBLIC_KEYS:
        resp = requests.get(GOOGLE_PUBLIC_KEY_URL).json()
        for key in resp['keys']:
           GOOGLE_PUBLIC_KEYS[key['kid']] = key 
        LAST_KEY_FETCH = int(time())

    return GOOGLE_PUBLIC_KEYS

# def _decode_google_user_token(token, aud=None):
#     idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
#     return idinfo

def _decode_google_user_token(token, aud=None):
    header = jwt.get_unverified_header(token)
    keys = _fetch_public_keys()
    # print(header)
    # print(keys)
    # cert_obj = load_pem_x509_certificate(
    #     keys[header['kid']].encode(), default_backend())
    options = {}
    if not aud:
        options['verify_aud'] = False
    payload = jwt.decode(token, keys[header['kid']],
                         audience=aud,
                         algorithms=[header['alg']],
                         options=options)
    return payload
