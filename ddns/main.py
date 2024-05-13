from ipaddress import IPv4Address
import client
from conf import CONF, ConfRecord


def conf_to_dns(conf_record: ConfRecord, domain: str, public_ip: IPv4Address):
    match conf_record.type:
        case "A":
            default_content = str(public_ip)
        case "CNAME":
            default_content = domain

    return client.DNSRecord(
        name=conf_record.name,
        type=conf_record.type,
        content=conf_record.content or default_content,
    )


# public_ip = client.get_public_ip()
public_ip = IPv4Address("152.37.72.135")


conf_records = [
    conf_to_dns(record, domain, public_ip)
    for domain, records in CONF.dns_records.items()
    for record in records
]


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
