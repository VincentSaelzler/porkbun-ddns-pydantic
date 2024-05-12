from ipaddress import IPv4Address
from typing import Literal
from pydantic import BaseModel
import requests
from conf import CONF, DNSRecord

GetEndpoint = Literal["ping", "retrieve"]
SetEndpoint = Literal["editByNameType"]


class Response(BaseModel):
    # raises exception for any other status
    status: Literal["SUCCESS"]


class PingResponse(Response):
    # ipv6 (AAAA) dns host records not supported
    yourIp: IPv4Address


class PorkbunDNSRecord(DNSRecord):
    id: str


class DomainResponse(Response):
    records: list[PorkbunDNSRecord]


class Body(BaseModel):
    apikey: str
    secretapikey: str


class Request(BaseModel):
    url: str
    body: Body


# send/receive http data
def http_post(request: Request):

    testjson = {
        "apikey": "pk1_895067c0e864a1820263c61fc5b05290d175f4ce4d0641c09c86a8e95e40cf5b",
        "secretapikey": "sk1_80b3bd38147b17b7cef1fb09e548ba39895d595d106217c73ea960c2145d7978",
    }

    # send via http
    response = requests.post(request.url, json=request.body.model_dump())
    # response = requests.post(request.url, json=testjson)

    try:
        # return content if request was successful
        response.raise_for_status()
        return response.content
    finally:
        # strip secrets
        # payload_without_secrets = payload.copy()
        # payload_without_secrets["secretapikey"] = "[redacted]"
        # payload_without_secrets["apikey"] = "[redacted]"

        # debugging output
        # print(url)
        # print(payload_without_secrets)
        # print(response.text)
        pass


# parse logical request to http request
def generate_http_request(endpoint: GetEndpoint):
    match endpoint:
        case "ping":
            return Request(
                url="/".join([str(CONF.ipv4_endpoint), endpoint]),
                body=Body(apikey=CONF.apikey, secretapikey=CONF.secretapikey),
            )
        case "retrieve":
            raise ValueError


# def parse_json_response(endpoint: GetEndpoint):
#     match endpoint:
#         case "ping":
#             return "x"
#         case
# # parse logical request to http request
# def generate_set_request(endpoint: SetEndpoint, domain: str, record: DNSRecord):

#     json_ = record.model_dump()
#     json_.update(API_KEYS)

#     subdomain_with_final_dot = record.name.replace(domain, "")
#     subdomain = subdomain_with_final_dot[:-1]

#     match endpoint, subdomain:
#         case "editByNameType", "":
#             return ("/".join([DNS_ENDPOINT, endpoint, domain, record.type]), json_)
#         case "editByNameType", str():
#             return (
#                 "/".join([DNS_ENDPOINT, endpoint, domain, record.type, subdomain]),
#                 json_,
#             )


# # validate json response
# def ping(raw_json: bytes):
#     return PingResponse.model_validate_json(raw_json).yourIp


# def retrieve(raw_json: bytes):
#     records = DomainResponse.model_validate_json(raw_json).records
#     # leave NS records unchanged; do not process
#     return [r for r in records if r.type != "NS"]


# # # case "update":
# # request_payload = {
# #     "content": "137.220.108.97",
# #     "name": "quercusphellos.online",
# #     "answer": "137.220.108.97",
# # }
# # request_payload.update(API_KEYS)
