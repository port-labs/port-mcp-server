from typing import Any


def inline_schema(schema: dict[str, Any]) -> dict[str, Any] | list[Any] | Any:
    defs = schema.pop("$defs", {})

    def replace_refs(obj: Any) -> dict[str, Any] | list[Any] | Any:
        if isinstance(obj, dict):
            if "$ref" in obj:
                ref_path = obj["$ref"].split("/")[-1]
                return replace_refs(defs[ref_path])
            else:
                return {k: replace_refs(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [replace_refs(item) for item in obj]
        return obj

    return replace_refs(schema)
