from pathlib import Path

from loadcredential import Credentials
from pydantic import HttpUrl

import ddns.model as model

# conf.json must be in the same directory as this (conf.py) file
_CONFIG_FILE = Path(__file__).parent / "conf.json"


class ConfigRecord(model.FrozenModel):
    name: str
    type: model.EditableDNSRecordType
    content: str | None = None

    def with_default_content(self, domain: str, public_ip: str):
        def default_content():
            match self.type:
                case "A":
                    return str(public_ip)
                case "CNAME":
                    return domain

        return type(self)(
            name=self.name,
            type=self.type,
            content=self.content or default_content(),
        )


class Configuration(model.FrozenModel):
    # apikey: EnvStr
    # secretapikey: EnvStr
    ipv4_endpoint: HttpUrl
    dns_endpoint: HttpUrl
    dns_records: dict[str, list[ConfigRecord]]


def get_configuration():
    with open(_CONFIG_FILE, "r") as f:
        config_file_contents = f.read()
        return Configuration.model_validate_json(config_file_contents, strict=True)


def get_porkbun_credential():
    credentials = Credentials()

    s = credentials["PORKBUN_SECRET_API_KEY"]
    a = credentials["PORKBUN_API_KEY"]

    return model.PorkbunCredential(secretapikey=s, apikey=a)


PORKBUN_CRED = get_porkbun_credential()
CONF = get_configuration()
