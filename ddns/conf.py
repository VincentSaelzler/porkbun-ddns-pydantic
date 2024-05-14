import os
from pydantic import BaseModel, BeforeValidator, ConfigDict, HttpUrl, ValidationInfo
from typing import Annotated, Any
from pathlib import Path

import model

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


class ConfigRecord(BaseModel):
    name: str
    type: model.RecordType
    content: str | None = None


class Configuration(BaseModel):
    model_config = ConfigDict(frozen=True)
    apikey: EnvStr
    secretapikey: EnvStr
    ipv4_endpoint: HttpUrl
    dns_endpoint: HttpUrl
    dns_records: dict[str, list[ConfigRecord]]


def GetConfiguration():
    with open(_CONFIG_FILE, "r") as f:
        config_file_contents = f.read()
        return Configuration.model_validate_json(config_file_contents, strict=True)


CONF = GetConfiguration()
