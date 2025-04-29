from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pydantic import ValidationError

from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.utils import logger
from src.utils.schema import inline_schema


@dataclass
class Tool:
    name: str
    description: str
    function: Callable[[BaseModel], dict[str, Any]]
    input_schema: BaseModel
    output_schema: BaseModel
    annotations: Annotations | None = None

    @property
    def input_schema_json(self):
        return inline_schema(self.input_schema.model_json_schema())

    @property
    def output_schema_json(self):
        return inline_schema(self.output_schema.model_json_schema())

    def validate_output(self, output: dict[str, Any]) -> BaseModel:
        logger.info(f"Validating output: {output}")
        try:
            return self.output_schema(**output)
        except ValidationError as e:
            message = f"Invalid output: {e.errors()}"
            logger.error(message)
            raise ValueError(message) from None

    def validate_input(self, input: dict[str, Any]) -> BaseModel:
        logger.info(f"Validating input: {input}")
        try:
            return self.input_schema(**input)
        except ValidationError as e:
            message = f"Invalid input: {e.errors()}"
            logger.error(message)
            raise ValueError(message) from None
