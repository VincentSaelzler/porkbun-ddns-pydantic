from typing import Any
import requests


def post(url: str, json: dict[str, Any]):
    r = requests.post(url, json=json)
    r.raise_for_status()
    return r.content
