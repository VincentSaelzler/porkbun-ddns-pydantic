import os
from pathlib import Path
from typing import Annotated, Any

import model
from pydantic import BeforeValidator, HttpUrl, ValidationInfo

# conf.json must be in the same directory as this (conf.py) file
_CONFIG_FILE = Path(__file__).parent / "conf.json"


def get_from_env(v: Any, info: ValidationInfo) -> str:
    """
    prioritize values in _CONFIG_FILE
    if unset, get from OS environment variables
    fail if non-existent in both locations
    """
    match info.field_name, v:
        case str() as field_name, str() | None:
            # prioritize the setting in _CONFIG_FILE
            # then check environment variables
            return v or os.environ[field_name.upper()]
        case str(), _:
            raise TypeError("incoming value must be str | None")
        case None, _:
            raise RuntimeError("unable to determine field name")


EnvStr = Annotated[str, BeforeValidator(get_from_env)]


class ConfigRecord(model.FrozenModel):
    name: str
    type: model.EditableRecordType
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
    apikey: EnvStr
    secretapikey: EnvStr
    ipv4_endpoint: HttpUrl
    dns_endpoint: HttpUrl
    dns_records: dict[str, list[ConfigRecord]]


def get_configuration():
    with open(_CONFIG_FILE, "r") as f:
        config_file_contents = f.read()
        return Configuration.model_validate_json(config_file_contents, strict=True)


CONF = get_configuration()
