import os
from pydantic import AfterValidator, BaseModel, HttpUrl, ValidationInfo
from typing import Annotated, Literal
from pathlib import Path


# conf.json must be in the same directory as this (conf.py) file
_CONFIG_FILE = Path(__file__).parent / "conf.json"


def get_from_env(s: str, info: ValidationInfo) -> str:
    """
    prioritize values in _CONFIG_FILE
    if unset, get from OS environment variables
    fail if non-existent in both locations
    """
    match info.field_name:
        case str():
            # prioritize the setting in _CONFIG_FILE
            if s != "":
                return s
            # check environment variables
            var_name = info.field_name.upper()
            return os.environ[var_name]
        case None:
            raise RuntimeError("unable to determine field name")


EnvStr = Annotated[str, AfterValidator(get_from_env)]


class DNSRecord(BaseModel):
    name: str
    type: Literal["NS", "A", "CNAME"]
    content: str


class Configuration(BaseModel):
    apikey: EnvStr
    secretapikey: EnvStr
    ipv4_endpoint: HttpUrl
    dns_endpoint: HttpUrl
    dns_records: list[DNSRecord]


def GetConfiguration():
    with open(_CONFIG_FILE, "r") as f:
        config_file_contents = f.read()
        return Configuration.model_validate_json(config_file_contents, strict=True)


CONF = GetConfiguration()


print("k")
