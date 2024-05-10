from typing import Callable, Literal
from functools import partial
import requests
from config import API_KEYS, IPV4_ENDPOINT, DNS_ENDPOINT

GetEndpoint = Literal["ping", "retrieve"]
Backend = Callable[[str, dict[str, str]], bytes]


def _post(url: str, json: dict[str, str]):
    r = requests.post(url, json=json)
    r.raise_for_status()
    return r.content


def _get(backend: Backend, endpoint: GetEndpoint, domain: str | None = None):
    match endpoint, domain:
        case "ping", _:
            return backend("/".join([IPV4_ENDPOINT, endpoint]), API_KEYS)
        case "retrieve", str():
            return _post("/".join([DNS_ENDPOINT, endpoint, domain]), API_KEYS)
        case "retrieve", None:
            raise ValueError("domain is required for retrieve endpoint")


get_http = partial(_get, backend=_post)

ip = get_http("ping", None)

ip = _get(_post, "ping", "quercusphellos.online")
# ip = get("ping", None)
# records = get("retrieve", "quercusphellos.online")
# records = get("retrieve", None)

print("wait")
