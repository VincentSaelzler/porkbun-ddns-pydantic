from typing import Callable, Literal
from functools import partial
import requests
from config import API_KEYS, IPV4_ENDPOINT, DNS_ENDPOINT

GetEndpoint = Literal["ping", "retrieve"]
Backend = Callable[[str, dict[str, str]], bytes]


# send/receive http data
def _post(url: str, json: dict[str, str]):
    r = requests.post(url, json=json)
    r.raise_for_status()
    return r.content


# parse logical request to http request
def _get(backend: Backend, endpoint: GetEndpoint, domain: str | None = None):
    match endpoint, domain:
        case "ping", _:
            return backend("/".join([IPV4_ENDPOINT, endpoint]), API_KEYS)
        case "retrieve", str():
            return _post("/".join([DNS_ENDPOINT, endpoint, domain]), API_KEYS)
        case "retrieve", None:
            raise ValueError("domain is required for retrieve endpoint")

get_http = partial(_get, _post)
# ip = get_http("ping", None)

# validate json response
def _validate(raw_json: bytes, get_endpoint: GetEndpoint):
    match get_endpoint:
        case "ping":
            # return public ipv4 address as string
            # ping_response = PingResponse.model_validate_json(response_content)
            # return str(ping_response.yourIp)
            pass
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



