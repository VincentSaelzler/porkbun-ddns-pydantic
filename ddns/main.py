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


def main():
    public_ip = client_mock.get_public_ip()
    for domain in CONF.dns_records:

        # get desired records
        config_records = CONF.dns_records[domain]
        config_records_with_defaults = [
            r.with_default_content(domain, public_ip) for r in config_records
        ]
        desired_records = models_to_record_set(config_records_with_defaults)

        # get porkbun records
        raw_porkbun_records = client_mock.get_records(domain)
        # check that no duplicate records exist
        _ = models_to_record_set(raw_porkbun_records)
        existing_records = {
            model_to_record(raw_record): raw_record
            for raw_record in raw_porkbun_records
        }

        print("done with main function")


if __name__ == "__main__":

    main()
    print("done with main script")
