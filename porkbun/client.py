from ipaddress import IPv4Address
from typing import Callable, Literal
from functools import partial
from pydantic import BaseModel
import requests
from config import API_KEYS, IPV4_ENDPOINT, DNS_ENDPOINT

GetEndpoint = Literal["ping", "retrieve"]
Backend = Callable[[str, dict[str, str]], bytes]


class Response(BaseModel):
    # raises exception for any other status
    status: Literal["SUCCESS"]


class PingResponse(Response):
    # ipv6 (AAAA) dns host records not supported
    yourIp: IPv4Address


# send/receive http data
def http(url: str, json: dict[str, str]):
    r = requests.post(url, json=json)
    r.raise_for_status()
    return r.content


# parse logical request to http request
def _get(backend: Backend, endpoint: GetEndpoint, domain: str | None = None):
    match endpoint, domain:
        case "ping", _:
            return backend("/".join([IPV4_ENDPOINT, endpoint]), API_KEYS)
        case "retrieve", str():
            return http("/".join([DNS_ENDPOINT, endpoint, domain]), API_KEYS)
        case "retrieve", None:
            raise ValueError("domain is required for retrieve endpoint")


get_http = partial(_get, http)
# ip = get_http("ping", None)


# validate json response
def validate(endpoint: GetEndpoint, raw_json: bytes):
    match endpoint:
        case "ping":
            return PingResponse.model_validate_json(raw_json).yourIp
        case "retrieve":
            # domain_response = DomainResponse.model_validate_json(response_content)
            # return domain_response
            raise NotImplementedError()
        # case "update":
        # request_payload = {
        #     "content": "137.220.108.97",
        #     "name": "quercusphellos.online",
        #     "answer": "137.220.108.97",
        # }
        # request_payload.update(API_KEYS)
