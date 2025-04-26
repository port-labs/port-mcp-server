from typing import Any

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict as PydanticConfigDict

class BaseModel(PydanticBaseModel):
    model_config = PydanticConfigDict(validate_by_name=True, validate_by_alias=True,serialize_by_alias=True)
    class ConfigDict:
        @staticmethod
        def json_schema_extra(schema: dict[str, Any], model: Any) -> None:
            schema.pop("title", None)
            if schema.get("default") is None:
                schema.pop("default", None)
            for prop in schema.get("properties", {}).values():
                prop.pop("title", None)
                if prop.get("default", None) is None:
                    prop.pop("default", None)
