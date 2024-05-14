from typing import Literal

from pydantic import BaseModel, ConfigDict

RecordType = Literal["CNAME", "A"]


class FrozenModel(BaseModel):
    model_config = ConfigDict(frozen=True)


class RecordItentifier(FrozenModel):
    name: str
    type: RecordType
    content: str | None
