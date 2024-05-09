import os
from ipaddress import IPv4Address
from typing import Any, Literal

from pydantic import BaseModel
import requests

_DNS_ENDPOINT = "https://porkbun.com/api/json/v3/dns"
_KEYS = {"apikey": os.environ["APIKEY"], "secretapikey": os.environ["SECRETAPIKEY"]}


class Response(BaseModel):
    # raises exception for any other status
    status: Literal["SUCCESS"]


class PingResponse(Response):
    # ipv6 (AAAA) dns host records not supported
    yourIp: IPv4Address


class Record(BaseModel):
    id: str
    name: str
    type: Literal["NS", "A"]
    content: str
    ttl: str
    prio: str | None
    notes: str | None


class DomainResponse(Response):
    records: list[Record]


def _post(url: str, json: dict[str, Any]):
    r = requests.post(url, json=_KEYS)
    r.raise_for_status()
    return r.content


def get_public_ip():

    # ipv4-specific endpoint
    PING_ENDPOINT = "https://api-ipv4.porkbun.com/api/json/v3/ping"

    # ping porkbun
    response_content = _post(PING_ENDPOINT, _KEYS)

    # return public ipv4 address as string
    ping_response = PingResponse.model_validate_json(response_content)
    return str(ping_response.yourIp)


def get_domain(domain: str):

    endpoint = _DNS_ENDPOINT + "/retrieve/" + domain

    response_content = _post(endpoint, _KEYS)

    domain_response = DomainResponse.model_validate_json(response_content)
    return domain_response


def get_records(domain: str, type: str, subdomain: str | None = None):
    endpoint = f"{_DNS_ENDPOINT}/retrieveByNameType/{domain}/{type}"
    if subdomain is not None:
        endpoint = f"{endpoint}/{subdomain}"
        
    response_content = _post(endpoint, _KEYS)
    
    domain_response = DomainResponse.model_validate_json(response_content)
    

    print("waittt")
