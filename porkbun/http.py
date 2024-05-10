import requests
from config import API_KEYS


_IPV4_ENDPOINT = "https://api-ipv4.porkbun.com/api/json/v3/"


def _send_request(url: str, json: dict[str, str]):
    r = requests.post(url, json=json)
    r.raise_for_status()
    return r.content


r = _send_request(_IPV4_ENDPOINT + "ping", API_KEYS)
print("wait")