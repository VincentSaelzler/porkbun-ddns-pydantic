from typing import Literal, Protocol

import porkbun.http
import porkbun.mockapi



class PorkbunClient:


    def __init__(self, backend_type: BackendType = "http") -> None:
        self._backend = PorkbunClient._backends[backend_type]

    def set_backend(self, backend_type: BackendType):
        self._backend = PorkbunClient._backends[backend_type]

    def get_public_ip(self) -> str: ...


# _DNS_ENDPOINT = "https://porkbun.com/api/json/v3/dns"


# class Response(BaseModel):
#     # raises exception for any other status
#     status: Literal["SUCCESS"]


# class PingResponse(Response):
#     # ipv6 (AAAA) dns host records not supported
#     yourIp: IPv4Address


# class Record(BaseModel):
#     id: str
#     name: str
#     type: Literal["NS", "A"]
#     content: str
#     ttl: str
#     prio: str | None
#     notes: str | None


# class DomainResponse(Response):
#     records: list[Record]


# def _post(url: str, json: dict[str, Any]):
#     r = requests.post(url, json=json)
#     r.raise_for_status()

#     print(r.text)
#     return r.content


def get_public_ip():
    # ping porkbun
    response_content = backend.get_public_ip()

    # return public ipv4 address as string
    ping_response = PingResponse.model_validate_json(response_content)
    return str(ping_response.yourIp)


# def get_domain(domain: str):

#     endpoint = _DNS_ENDPOINT + "/retrieve/" + domain

#     response_content = _post(endpoint, API_KEYS)

#     domain_response = DomainResponse.model_validate_json(response_content)
#     return domain_response


# # def get_records(domain: str, type: str, subdomain: str | None = None):
# #     endpoint = f"{_DNS_ENDPOINT}/retrieveByNameType/{domain}/{type}"
# #     if subdomain is not None:
# #         endpoint = f"{endpoint}/{subdomain}"

# #     response_content = _post(endpoint, _KEYS)

# #     domain_response = DomainResponse.model_validate_json(response_content)


# def set_records(domain: str, type: str, subdomain: str | None = None):
#     endpoint = f"{_DNS_ENDPOINT}/editByNameType/{domain}/{type}"
#     if subdomain is not None:
#         endpoint = f"{endpoint}/{subdomain}"

#     request_payload = {
#         "content": "137.220.108.97",
#         "name": "quercusphellos.online",
#         "answer": "137.220.108.97",
#     }
#     request_payload.update(API_KEYS)

#     response_content = _post(endpoint, request_payload)

#     domain_response = DomainResponse.model_validate_json(response_content)

#     print("waittt")
