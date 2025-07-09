from ipaddress import IPv4Address
from typing import Literal, Union, get_args

import requests
from pydantic import SerializeAsAny

from ddns.conf import CONF, PORKBUN_CRED
from ddns.model import DNSRecord, EditableDNSRecordType, FrozenModel

GetEndpoint = Literal["ping", "retrieve"]
SetEndpoint = Literal["create", "delete"]


# unmanaged types will be left as-is on porkbun
UnmanagedRecordType = Literal["MX", "ALIAS", "TXT", "NS", "AAAA", "SRV", "TLSA", "CAA"]


class Response(FrozenModel):
    # raises exception for any other status
    status: Literal["SUCCESS"]


class PingResponse(Response):
    # ipv6 (AAAA) dns host records not supported
    yourIp: IPv4Address


class PorkbunRecord(FrozenModel):
    id: str
    name: str
    type: EditableDNSRecordType | UnmanagedRecordType
    content: str


class DomainResponse(Response):
    records: list[PorkbunRecord]


class Body(FrozenModel):
    apikey: str
    secretapikey: str


class CreateBody(Body):
    name: str
    type: EditableDNSRecordType
    content: str


class Request(FrozenModel):
    url: str
    body: SerializeAsAny[Body]


# send/receive http data
def _http_post(request: Request):
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
def _generate_get_request(endpoint: GetEndpoint, domain: str | None = None):
    match endpoint, domain:
        case "ping", _:
            return Request(
                url="/".join([str(CONF.ipv4_endpoint), endpoint]),
                body=Body(
                    apikey=PORKBUN_CRED.apikey, secretapikey=PORKBUN_CRED.secretapikey
                ),
            )
        case "retrieve", str():
            return Request(
                url="/".join([str(CONF.dns_endpoint), endpoint, domain]),
                body=Body(
                    apikey=PORKBUN_CRED.apikey, secretapikey=PORKBUN_CRED.secretapikey
                ),
            )
        case "retrieve", None:
            raise ValueError("domain is required for retrieve endpoint")


def _compute_name(domain: str, raw_name: str):
    # external links are not allowed
    if not raw_name.endswith(domain):
        raise ValueError(f"must be a subdomain (or wildcard record) within {domain}")
    # root domain
    if raw_name == domain:
        return ""
    # wildcard
    if raw_name.startswith("*"):
        return "*"
    # subdomain
    domain_with_leading_dot = "." + domain
    return raw_name.replace(domain_with_leading_dot, "")


def _generate_set_request(
    endpoint: SetEndpoint, domain: str, record: Union[PorkbunRecord, DNSRecord]
):

    match endpoint, record:
        case "create", DNSRecord():
            body = CreateBody(
                apikey=PORKBUN_CRED.apikey,
                secretapikey=PORKBUN_CRED.secretapikey,
                name=_compute_name(domain, record.name),
                type=record.type,
                content=record.content,
            )
            return Request(
                url="/".join([str(CONF.dns_endpoint), endpoint, domain]),
                body=body,
            )
        case "create", PorkbunRecord():
            raise TypeError("create endpoint requires a record of type model.Record")
        case "delete", PorkbunRecord():
            return Request(
                url="/".join([str(CONF.dns_endpoint), endpoint, domain, record.id]),
                body=Body(
                    apikey=PORKBUN_CRED.apikey, secretapikey=PORKBUN_CRED.secretapikey
                ),
            )
        case "delete", DNSRecord():
            raise TypeError(
                "create endpoint requires a record of type client.PorkbunRecord"
            )
        case _:
            # https://discuss.python.org/t/how-can-you-match-on-a-union-of-types/26785/6
            raise RuntimeError(
                "i don't think this can happen, but the static type checker says it can"
            )


def get_public_ip():
    request = _generate_get_request("ping")
    response = _http_post(request)
    return str(PingResponse.model_validate_json(response).yourIp)


def get_records(domain: str):
    request = _generate_get_request("retrieve", domain)
    response = _http_post(request)
    records = DomainResponse.model_validate_json(response).records
    # only return records that the app can create/update/delete
    # other records (e.g. NS records) are left as-is
    # HACK get_args is really sensitive to how EditableDNSRecordType is defined
    editable_records = [r for r in records if r.type in get_args(EditableDNSRecordType)]
    return editable_records


def create_record(domain: str, record: DNSRecord):
    request = _generate_set_request("create", domain, record)
    response = _http_post(request)
    # check for success response
    _ = Response.model_validate_json(response)


def delete_record(domain: str, record: PorkbunRecord):
    request = _generate_set_request("delete", domain, record)
    response = _http_post(request)
    # check for success response
    _ = Response.model_validate_json(response)
