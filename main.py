from typing import Protocol

import porkbun.httpclient
import porkbun.mockclient


class Client(Protocol):
    @staticmethod
    def get_public_ip() -> str: ...
    @staticmethod
    def get_domain(domain: str) -> porkbun.httpclient.DomainResponse: ...
    @staticmethod
    def get_records(domain: str, type: str, subdomain: str | None = None) -> None: ...


httpclient: Client = porkbun.httpclient
mockclient: Client = porkbun.mockclient

# public_ip = httpclient.get_public_ip()
# domain_records = mockclient.get_domain("quercusphellos.online")

output = httpclient.get_records("quercusphellos.online", "A")


print("yahoo")
