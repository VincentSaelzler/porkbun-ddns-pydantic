from ipaddress import IPv4Address
from typing import Any, Literal
from pydantic import BaseModel, TypeAdapter
import requests
from config import API_KEYS, IPV4_ENDPOINT, DNS_ENDPOINT
from json import dumps

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


class CallAndResponse(BaseModel):
    url: str
    payload: dict[str, Any]
    response: bytes


def json_post(url: str, payload: dict[str, Any]):
    with open("porkbun/call_log.json", "r") as f:
        file_content = f.read()
        call_log_adapter = TypeAdapter(list[CallAndResponse])
        call_log = call_log_adapter.validate_json(file_content)
        print(call_log)
    

# send/receive http data
def http_post(url: str, payload: dict[str, Any]):

    # send via http
    r = requests.post(url, json=payload)

    try:
        # return content if request was successful
        r.raise_for_status()
        return r.content
    finally:
        call_and_response = CallAndResponse(url=url, payload=payload, response=r.content)
        print(CallAndResponse.model_dump_json(call_and_response))


# parse logical request to http request
def generate_get_request(endpoint: GetEndpoint, domain: str | None = None):
    match endpoint, domain:
        case "ping", _:
            return ("/".join([IPV4_ENDPOINT, endpoint]), API_KEYS)
        case "retrieve", str():
            return ("/".join([DNS_ENDPOINT, endpoint, domain]), API_KEYS)
        case "retrieve", None:
            raise ValueError("domain is required for retrieve endpoint")


# parse logical request to http request
def generate_set_request(endpoint: SetEndpoint, domain: str, record: Record):

    json_ = record.model_dump()
    json_.update(API_KEYS)

    subdomain_with_final_dot = record.name.replace(domain, "")
    subdomain = subdomain_with_final_dot[:-1]

    match endpoint, subdomain:
        case "editByNameType", "":
            return ("/".join([DNS_ENDPOINT, endpoint, domain, record.type]), json_)
        case "editByNameType", str():
            return (
                "/".join([DNS_ENDPOINT, endpoint, domain, record.type, subdomain]),
                json_,
            )


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
