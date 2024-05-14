from ipaddress import IPv4Address

from client import PorkbunRecord


def get_public_ip():
    return IPv4Address("4.20.4.20")


def get_records(domain: str):
    match domain:
        case "quercusphellos.online":
            return [
                PorkbunRecord(
                    id="399347448",
                    name="quercusphellos.online",
                    type="A",
                    content="137.220.108.97",
                ),
                PorkbunRecord(
                    id="399348596",
                    name="www.quercusphellos.online",
                    type="CNAME",
                    content="quercusphellos.online",
                ),
            ]
        case _:
            raise NotImplementedError()