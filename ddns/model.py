from typing import Literal

from pydantic import BaseModel, ConfigDict

EditableRecordType = Literal["CNAME", "A"]


class FrozenModel(BaseModel):
    model_config = ConfigDict(frozen=True)


class Record(FrozenModel):
    name: str
    type: EditableRecordType
    content: str | None
