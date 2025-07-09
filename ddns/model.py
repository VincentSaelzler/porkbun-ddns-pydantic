from typing import Literal

from pydantic import BaseModel, ConfigDict

EditableDNSRecordType = Literal["CNAME", "A"]


class FrozenModel(BaseModel):
    model_config = ConfigDict(frozen=True)


class DNSRecord(FrozenModel):
    name: str
    type: EditableDNSRecordType
    content: str


class PorkbunCredential(FrozenModel):
    secretapikey: str
    apikey: str
