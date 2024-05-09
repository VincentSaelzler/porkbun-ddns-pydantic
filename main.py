from typing import Protocol

import porkbun.httpclient
import porkbun.mockclient


class Client(Protocol):
    @staticmethod
    def get_public_ip() -> str: ...
    @staticmethod
    def get_domain(domain: str) -> porkbun.httpclient.DomainResponse: ...


httpclient: Client = porkbun.httpclient
mockclient: Client = porkbun.mockclient

public_ip = mockclient.get_public_ip()
domain_records = mockclient.get_domain("quercusphellos.online")

print("yahoo")
