from typing import Any
from pydantic import BaseModel

class BaseModel(BaseModel):
    class Config:
        @staticmethod
        def json_schema_extra(schema: dict[str, Any], model: Any) -> None:
            schema.pop('title', None)
            if schema.get('default',None) == None:
                schema.pop('default', None)
            for prop in schema.get('properties', {}).values():
                prop.pop('title', None)
                if prop.get('default',None) == None:
                    prop.pop('default', None)
