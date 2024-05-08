import os
import requests

_KEYS = {"apikey": os.environ["APIKEY"], "secretapikey": os.environ["SECRETAPIKEY"]}
_BASE_ENDPOINT = "https://porkbun.com/api/json/v3"


def get_public_ip():
    endpoint = _BASE_ENDPOINT + "/ping"
    r = requests.post(endpoint, data=_KEYS)
    r.raise_for_status()
    print("ok")
