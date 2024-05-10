from ipaddress import IPv4Address
import os
from typing import Literal

from pydantic import BaseModel

MOCKFILE_DIR = "porkbun/mockfiles/"
API_KEYS = {"apikey": os.environ["APIKEY"], "secretapikey": os.environ["SECRETAPIKEY"]}

IPV4_ENDPOINT = "https://api-ipv4.porkbun.com/api/json/v3"
DNS_ENDPOINT = "https://porkbun.com/api/json/v3/dns"


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