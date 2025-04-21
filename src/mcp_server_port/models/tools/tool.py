from typing import Callable
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from loguru import logger
from src.mcp_server_port.models.common.base_pydantic import BaseModel
from pydantic import ValidationError

from src.mcp_server_port.utils.schema import inline_schema
import mcp.types as types
@dataclass
class Tool:
    name: str
    description: str
    # attributes: dict[str, Any]
    function: Callable[[BaseModel], Dict[str, Any]]
    input_schema: BaseModel
    output_schema: BaseModel

    @property
    def inputSchema(self):
        return inline_schema(self.input_schema.model_json_schema())
    
    @property
    def outputSchema(self):
        return inline_schema(self.output_schema.model_json_schema())
    
    def validate_output(self, output: Dict[str, Any]) -> BaseModel:
        logger.info(f"Validating output: {output}")
        try:
            return self.output_schema(**output)
        except ValidationError as e:
            # logger.error(f"Invalid output: {e}")
            raise ValueError(f"Invalid output")
    
    def validate_input(self, input: Dict[str, Any]) -> BaseModel:
        logger.info(f"Validating input: {input}")
        try:
            return self.input_schema(**input)
        except ValidationError as e:
            # Extract useful information from the validation error
            errors = e.errors()
            error_details = []
            
            for error in errors:
                # Get the location of the error (which field/path)
                loc = ".".join(str(l) for l in error["loc"])
                
                # Get value that caused the error
                input_value = error.get("input")
                
                # Get error type and message
                error_type = error.get("type")
                msg = error.get("msg")
                
                # Get the expected valid values if available
                expected_values = None
                if error_type == "literal_error" and "ctx" in error:
                    expected_values = error.get("ctx", {}).get("expected")
                
                # Create a helpful error message
                error_detail = {
                    "field": loc,
                    "error_type": error_type,
                    "message": msg,
                    "input_value": input_value
                }
                
                if expected_values:
                    error_detail["expected_values"] = expected_values
                    
                error_details.append(error_detail)
            
            # Generate field-specific schema information
            schema_info = {}
            for error in errors:
                loc = error["loc"]
                if len(loc) > 0:
                    # Get the first level field name
                    field_name = str(loc[0])
                    
                    # Only add schema info if we haven't already for this field
                    if field_name not in schema_info:
                        # Try to get schema for this field
                        field_schema = self.input_schema.model_json_schema().get("properties", {}).get(field_name, {})
                        if field_schema:
                            schema_info[field_name] = field_schema
            
            # Create a structured error response with examples
            structured_error = {
                "errors": error_details,
                "schema_info": schema_info,
                "failed_validation": True
            }
            
            # Log the detailed error for debugging
            logger.error(f"Invalid input: {e}")
            logger.debug(f"Detailed validation errors: {structured_error}")
            
            # Raise with enhanced error message
            error_message = f"Invalid input: {str(e)}\nDetailed errors: {structured_error}"
            raise ValueError(error_message)
    