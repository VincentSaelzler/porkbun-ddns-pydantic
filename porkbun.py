import os
from ipaddress import IPv4Address
from typing import Literal

import requests
from pydantic import BaseModel


_DNS_ENDPOINT = "https://porkbun.com/api/json/v3/dns"
_KEYS = {"apikey": os.environ["APIKEY"], "secretapikey": os.environ["SECRETAPIKEY"]}


class Response(BaseModel):
    # raises exception for any other status
    status: Literal["SUCCESS"]


class PingResponse(Response):
    status: Literal["SUCCESS"]
    yourIp: IPv4Address


def get_public_ip():

    # ipv4-specific endpoint
    PING_ENDPOINT = "https://api-ipv4.porkbun.com/api/json/v3/ping"

    # ping porkbun
    r = requests.post(PING_ENDPOINT, json=_KEYS)
    r.raise_for_status()

    # capture public ipv4 address from response
    ping_response = PingResponse.model_validate_json(r.content)
    return ping_response.yourIp
