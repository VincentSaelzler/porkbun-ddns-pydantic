from ipaddress import IPv4Address
from typing import Literal
from pydantic import BaseModel
import requests
from config import API_KEYS, IPV4_ENDPOINT, DNS_ENDPOINT

GetEndpoint = Literal["ping", "retrieve"]
SetEndpoint = Literal["editByNameType"]
# Backend = Callable[[str, dict[str, str]], bytes]


class Response(BaseModel):
    # raises exception for any other status
    status: Literal["SUCCESS"]


class PingResponse(Response):
    # ipv6 (AAAA) dns host records not supported
    yourIp: IPv4Address


class Record(BaseModel):
    name: str
    type: Literal["NS", "A", "CNAME"]
    content: str


class DomainResponse(Response):
    records: list[Record]


# send/receive http data
def http_post(url: str, json_: dict[str, str]):
    r = requests.post(url, json=json_)
    r.raise_for_status()
    return r.content


# parse logical request to http request
def generate_get_request(endpoint: GetEndpoint, domain: str | None = None):
    match endpoint, domain:
        case "ping", _:
            return ("/".join([IPV4_ENDPOINT, endpoint]), API_KEYS)
        case "retrieve", str():
            return ("/".join([DNS_ENDPOINT, endpoint, domain]), API_KEYS)
        case "retrieve", None:
            raise ValueError("domain is required for retrieve endpoint")


# # parse logical request to http request
# def generate_set_request(
#     endpoint: SetEndpoint, domain: str, type_: str, subdomain: str | None = None
# ):
#     match endpoint, domain, type_, subdomain:
#         case "editByNameType", str(), str():
#             raise ValueError("domain is required for retrieve endpoint")


# validate json response
def ping(raw_json: bytes):
    return PingResponse.model_validate_json(raw_json).yourIp

def retrieve(raw_json: bytes):
    records = DomainResponse.model_validate_json(raw_json).records
    # leave NS records unchanged; do not process
    return [r for r in records if r.type != "NS"]

# # case "update":
# # request_payload = {
# #     "content": "137.220.108.97",
# #     "name": "quercusphellos.online",
# #     "answer": "137.220.108.97",
# # }
# # request_payload.update(API_KEYS)
