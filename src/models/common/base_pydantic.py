from typing import Any

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict as PydanticConfigDict


def json_schema_extra(schema: dict[str, Any], model: Any) -> None:
    schema.pop("title", None)
    for prop in schema.get("properties", {}).values():
        prop.pop("title", None)


class BaseModel(PydanticBaseModel):
    model_config = PydanticConfigDict(
        validate_by_name=True, validate_by_alias=True, serialize_by_alias=True, json_schema_extra=json_schema_extra
    )
