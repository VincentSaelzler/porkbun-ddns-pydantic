from ipaddress import IPv4Address

from pydantic import BaseModel

import client
import client_mock
from conf import CONF, ConfigRecord, RecordType


class EditableRecord(BaseModel):
    # https://github.com/pydantic/pydantic/issues/1303
    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    name: str
    type: RecordType
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


def deduplicate(editable_records: list[EditableRecord]):
    distinct_records = set(editable_records)
    if len(distinct_records) != len(editable_records):
        raise ValueError(f"no duplicate records allowed. input: {str(editable_records)}")
    return distinct_records


def conform_porkbun_record(porkbun_record: client.PorkbunRecord):
    return EditableRecord.model_validate(porkbun_record.model_dump())


def main():

    public_ip = client_mock.get_public_ip()
    for domain in CONF.dns_records:
        # desired configuration from conf.json file
        desired_records = deduplicate(
            [
                conform_config_record(record, domain, public_ip)
                for record in CONF.dns_records[domain]
            ]
        )
        # actual configuration from porkbun api
        actual_records = deduplicate(
            [
                conform_porkbun_record(record)
                for record in client_mock.get_records(domain)
            ]
        )
        _, _ = desired_records, actual_records
        print("done with main function")


if __name__ == "__main__":
    main()
    print("done with main script")
