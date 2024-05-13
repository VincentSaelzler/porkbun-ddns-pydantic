from ipaddress import IPv4Address
from typing import Literal
from pydantic import BaseModel
import requests
from conf import CONF, EditableRecordType, FixedRecordType


GetEndpoint = Literal["ping", "retrieve"]
SetEndpoint = Literal["editByNameType"]


class Response(BaseModel):
    # raises exception for any other status
    status: Literal["SUCCESS"]


class PingResponse(Response):
    # ipv6 (AAAA) dns host records not supported
    yourIp: IPv4Address


class PorkbunRecord(BaseModel):
    id: str
    name: str
    type: EditableRecordType | FixedRecordType
    content: str


class DomainResponse(Response):
    records: list[PorkbunRecord]


class Body(BaseModel):
    apikey: str
    secretapikey: str


class Request(BaseModel):
    url: str
    body: Body


# send/receive http data
def http_post(request: Request):
    # send via http
    response = requests.post(request.url, json=request.body.model_dump())
    try:
        # return content if request was successful
        response.raise_for_status()
        return response.content
    finally:
        print(
            request.model_dump_json(
                indent=2, exclude={"body": {"apikey", "secretapikey"}}
            )
        )
        print(response.text)


# parse logical request to http request
def generate_http_request(endpoint: GetEndpoint, domain: str | None = None):
    match endpoint, domain:
        case "ping", _:
            return Request(
                url="/".join([str(CONF.ipv4_endpoint), endpoint]),
                body=Body(apikey=CONF.apikey, secretapikey=CONF.secretapikey),
            )
        case "retrieve", str():
            return Request(
                url="/".join([str(CONF.dns_endpoint), endpoint, domain]),
                body=Body(apikey=CONF.apikey, secretapikey=CONF.secretapikey),
            )
        case "retrieve", None:
            raise ValueError("domain is required for retrieve endpoint")


def get_public_ip():
    request = generate_http_request("ping")
    response = http_post(request)
    return PingResponse.model_validate_json(response).yourIp


def get_records(domain: str):
    request = generate_http_request("retrieve", domain)
    response = http_post(request)
    records = DomainResponse.model_validate_json(response).records
    # leave NS records as-is; do not edit or delete
    editable_records = [r for r in records if r.type != "NS"]
    return editable_records


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
