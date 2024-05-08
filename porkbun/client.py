import os
from ipaddress import IPv4Address
from typing import Literal

from pydantic import BaseModel

import porkbun.mockapi as mockapi  # pyright: ignore[reportUnusedImport]
import porkbun.restapi as restapi  # pyright: ignore[reportUnusedImport]

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
    response = mockapi.post(PING_ENDPOINT, json=_KEYS)

    # return public ipv4 address as string
    ping_response = PingResponse.model_validate_json(response)
    return str(ping_response.yourIp)
