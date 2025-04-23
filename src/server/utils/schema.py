from typing import Any, Dict
from loguru import logger

def inline_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    defs = schema.pop("$defs", {})
    logger.info(f"defs: {defs}")
    def replace_refs(obj):
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