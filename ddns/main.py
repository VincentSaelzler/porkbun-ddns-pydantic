from typing import Sequence, TypeVar

import client
import client_mock
from conf import CONF
from model import BaseModel, Record
from pydantic import BaseModel

T = TypeVar("T")


def list_to_set(records: list[T]):
    distinct_records = set(records)
    if len(distinct_records) != len(records):
        raise ValueError(f"no duplicate records allowed. input: {str(records)}")
    return distinct_records


def records_to_record_set(records: list[Record]):
    return list_to_set(records)


def model_to_record(model: BaseModel):
    return Record.model_validate(model.model_dump())


def models_to_records(models: Sequence[BaseModel]):
    return [model_to_record(m) for m in models]


def models_to_record_set(models: Sequence[BaseModel]):
    return records_to_record_set(models_to_records(models))


def get_desired_records(domain: str, public_ip: str):
    config_records = CONF.dns_records[domain]
    config_records_with_defaults = [
        r.with_default_content(domain, public_ip) for r in config_records
    ]
    return models_to_record_set(config_records_with_defaults)


def get_existing_records(domain: str):
    porkbun_records = client_mock.get_records(domain)
    # check that no duplicate records exist
    _ = models_to_record_set(porkbun_records)
    return {model_to_record(raw_record): raw_record for raw_record in porkbun_records}


def main():
    public_ip = client_mock.get_public_ip()
    for domain in CONF.dns_records:

        # desired records from config file; existing records from porkbun
        desired_records = get_desired_records(domain, public_ip)
        existing_porkbun_records = get_existing_records(domain)
        existing_records = existing_porkbun_records.keys()

        # delete old records before creating new ones!
        for old_record in existing_records - desired_records:
            old_porkbun_record = existing_porkbun_records[old_record]
            print("delete ", old_porkbun_record.model_dump_json())

        # create new records
        for new_record in desired_records - existing_records:
            print("create ", new_record.model_dump_json())
            client.create_record(domain, new_record)

        # log records that stayed the same
        for matching_record in desired_records & existing_records:
            matching_porkbun_record = existing_porkbun_records[matching_record]
            print("keep ", matching_porkbun_record.model_dump_json())

        print("done with main function")


if __name__ == "__main__":
    main()
    print("done with main script")
