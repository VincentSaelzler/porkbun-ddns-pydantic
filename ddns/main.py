from ipaddress import IPv4Address

from pydantic import BaseModel

import client
import client_mock
from conf import CONF, ConfigRecord, EditableRecordType


class EditableRecord(BaseModel):
    name: str
    type: EditableRecordType
    content: str


def conform_config_record(
    conf_record: ConfigRecord, domain: str, public_ip: IPv4Address
):
    def default_content():
        match conf_record.type:
            case "A":
                return str(public_ip)
            case "CNAME":
                return domain

    return EditableRecord(
        name=conf_record.name,
        type=conf_record.type,
        content=conf_record.content or default_content(),
    )


def conform_porkbun_record(porkbun_record: client.PorkbunRecord):
    return EditableRecord.model_validate(porkbun_record.model_dump())


public_ip = client_mock.get_public_ip()
for domain in CONF.dns_records:
    # desired configuration from conf.json file
    desired_records = [
        conform_config_record(record, domain, public_ip)
        for record in CONF.dns_records[domain]
    ]
    # actual configuration from porkbun api
    actual_records = [record for record in client_mock.get_records(domain)]
    print("hoaky")

# url, json_ = client.generate_http_request("retrieve", "quercusphellos.online")
# response = client.http_post(url, json_)
# records = client.retrieve(response)

# url, json_ = client.generate_set_request(
#     "editByNameType", "quercusphellos.online", records[0]
# )
# response = client.http_post(url, json_)


# url, json_ = client.generate_set_request(
#     "editByNameType", "quercusphellos.online", records[1]
# )


# response = client.http_post(url, json_)
# response_bytes = client.get_http("ping", None)
# public_ip = client.get_ip(response_bytes)

# # response_bytes = client.get_http("retrieve", "quercusphellos.online")


print("more functional")
