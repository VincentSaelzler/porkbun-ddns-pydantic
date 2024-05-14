import client
import client_mock

# import client_mock
from conf import CONF, ConfigRecord

# from pydantic import BaseModel


def append_default_content(conf_record: ConfigRecord, domain: str, public_ip: str):
    def default_content():
        match conf_record.type:
            case "A":
                return str(public_ip)
            case "CNAME":
                return domain

    return ConfigRecord(
        name=conf_record.name,
        type=conf_record.type,
        content=conf_record.content or default_content(),
    )


# def deduplicate(editable_records: list[EditableRecord]):
#     distinct_records = set(editable_records)
#     if len(distinct_records) != len(editable_records):
#         raise ValueError(
#             f"no duplicate records allowed. input: {str(editable_records)}"
#         )
#     return distinct_records


# def conform_porkbun_record(porkbun_record: client.PorkbunRecord):
#     return EditableRecord.model_validate(porkbun_record.model_dump())


def main():
    public_ip = client_mock.get_public_ip()
    for domain in CONF.dns_records:

        config_records = [r for r in CONF.dns_records[domain]]
        config_records_with_defaults = [
            append_default_content(r, domain, public_ip) for r in config_records
        ]

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
