from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from pydantic import ValidationError

from src.models.common.annotations import Annotations
from src.models.common.base_pydantic import BaseModel
from src.utils import logger
from src.utils.schema import inline_schema

T = TypeVar("T", bound=BaseModel)


@dataclass
class Tool(Generic[T]):
    name: str
    description: str
    function: Callable[[T], Awaitable[dict[str, Any]]]
    input_schema: type[T]
    output_schema: type[BaseModel]
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

    def validate_input(self, input: dict[str, Any]) -> T:
        logger.info(f"Validating input: {input}")
        try:
            return self.input_schema(**input)
        except ValidationError as e:
            message = f"Invalid input: {e.errors()}"
            logger.error(message)
            raise ValueError(message) from None
