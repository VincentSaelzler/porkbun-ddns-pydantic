from typing import Protocol

import porkbun.httpclient
import porkbun.mockclient


class Client(Protocol):
    def get_public_ip(self) -> str: ...


httpclient: Client = porkbun.httpclient
mockclient: Client = porkbun.mockclient

public_ip = httpclient.get_public_ip()
mock_ip = mockclient.get_public_ip()

print("yahoo")
