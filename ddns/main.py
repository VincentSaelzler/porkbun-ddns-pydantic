import client
import client_mock
from conf import CONF, ConfigRecord
from model import RecordItentifier


def deduplicate(editable_records: list[ConfigRecord]):
    distinct_records = set(editable_records)
    if len(distinct_records) != len(editable_records):
        raise ValueError(
            f"no duplicate records allowed. input: {str(editable_records)}"
        )
    return distinct_records


# def conform_porkbun_record(porkbun_record: client.PorkbunRecord):
#     return EditableRecord.model_validate(porkbun_record.model_dump())


def main():
    public_ip = client_mock.get_public_ip()
    for domain in CONF.dns_records:

        config_records = [r for r in CONF.dns_records[domain]]
        config_records_with_defaults = [
            r.with_default_content(domain, public_ip) for r in config_records
        ]
        config_record_identifiers = [
            RecordItentifier.model_validate(r.model_dump())
            for r in config_records_with_defaults
        ]
        desired_records = set(config_record_identifiers)

        # config_records_with_defaults = [r for r in CONF.dns_records[domain]]
        # desired configuration from conf.json file
        # desired_records = deduplicate(

        #             [
        #                 conform_config_record(record, domain, public_ip)
        #                 for record in CONF.dns_records[domain]
        #             ]
        #         )
        #         # actual configuration from porkbun api
        #         actual_records = deduplicate(
        #             [
        #                 conform_porkbun_record(record)
        #                 for record in client_mock.get_records(domain)
        #             ]
        #         )
        #         _, _ = desired_records, actual_records
        print("done with main function")


if __name__ == "__main__":

    main()
    print("done with main script")
