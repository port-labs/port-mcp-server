from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from mcp.types import TextContent, GetPromptResult, PromptMessage

@dataclass
class PortToken:
    """Data model for Port authentication token."""
    access_token: str
    expires_in: int
    token_type: str

    def to_text(self) -> str:
        return f"""Authentication successful.
                Token: {self.access_token}
                Expires in: {self.expires_in} seconds
                Token type: {self.token_type}"""

    def to_prompt_result(self) -> GetPromptResult:
        return GetPromptResult(
            description="Port Authentication Token",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=self.to_text())
                )
            ]
        )

@dataclass
class PortBlueprint:
    """Data model for Port blueprint."""
    title: str
    identifier: str
    description: Optional[str] = None
    icon: Optional[str] = None
    schema: Optional[Dict[str, Any]] = None
    relations: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    created_by: Optional[str] = None
    updated_at: Optional[str] = None
    updated_by: Optional[str] = None
    
    def to_summary(self) -> str:
        """Returns a summary of the blueprint (title, identifier, description)."""
        desc = f"\nDescription: {self.description}" if self.description else ""
        return f"{self.title} (ID: {self.identifier}){desc}"
    
    def to_text(self, detailed: bool = True) -> str:
        """
        Returns a textual representation of the blueprint.
        
        Args:
            detailed: If True, includes schema details. If False, returns summary.
        """
        if not detailed:
            return self.to_summary()
            
        summary = self.to_summary()

        if self.schema and "properties" in self.schema:
            schema_text = "\nSchema:\n"
            for prop_id, prop_details in self.schema["properties"].items():
                prop_title = prop_details.get("title", "No Title")
                prop_type = prop_details.get("type", "No Type")
                prop_format = prop_details.get("format", "No Format")
                schema_text += f"- **{prop_id}**: {prop_title} (Type: {prop_type}, Format: {prop_format})\n"
        else:
            schema_text = ""
        
        relations_text = ""
        if self.relations:
            relations_text = "\nRelations:\n"
            for rel_id, rel_details in self.relations.items():
                rel_title = rel_details.get("title", "No Title")
                rel_target = rel_details.get("target", "No Target")
                rel_cardinality = "Many" if rel_details.get("many", False) else "Single"
                relations_text += f"- **{rel_id}**: {rel_title} (Target: {rel_target}, {rel_cardinality})\n"
        
        return f"{summary}{schema_text}{relations_text}"

@dataclass
class PortBlueprintList:
    """Data model for a list of Port blueprints."""
    blueprints: List[PortBlueprint] = field(default_factory=list)
    
    def to_text(self, detailed: bool = False) -> str:
        """
        Returns a textual representation of the blueprint list.
        
        Args:
            detailed: If True, includes detailed information for each blueprint.
        """
        if not self.blueprints:
            return "No blueprints found."
        
        result = "# Port Blueprints\n\n"
        for i, blueprint in enumerate(self.blueprints, 1):
            result += f"## {i}. {blueprint.to_text(detailed=detailed)}\n\n"
        
        return result

@dataclass
class PortEntity:
    """Data model for Port entity."""
    identifier: str
    title: str
    blueprint: str
    properties: Dict[str, Any] = field(default_factory=dict)
    relations: Dict[str, Any] = field(default_factory=dict)
    icon: Optional[str] = None
    team: Optional[List[str]] = None
    created_at: Optional[str] = None
    created_by: Optional[str] = None
    updated_at: Optional[str] = None
    updated_by: Optional[str] = None
    
    def to_summary(self) -> str:
        """Returns a summary of the entity (title, identifier, blueprint)."""
        return f"{self.title} (ID: {self.identifier})\nBlueprint: {self.blueprint}"
    
    def to_text(self, detailed: bool = True) -> str:
        """
        Returns a textual representation of the entity.
        
        Args:
            detailed: If True, includes properties, relations, and timestamps.
                     If False, returns summary.
        """
        if not detailed:
            return self.to_summary()
            
        result = f"# {self.to_summary()}\n"
        
        if self.properties:
            result += "\n## Properties\n"
            for key, value in self.properties.items():
                result += f"- {key}: {value}\n"
        
        if self.relations:
            result += "\n## Relations\n"
            for key, value in self.relations.items():
                result += f"- {key}: {value}\n"
        
        if self.created_at:
            result += f"\nCreated: {self.created_at}\n"
        if self.updated_at:
            result += f"Updated: {self.updated_at}\n"
        
        return result

@dataclass
class PortEntityList:
    """Data model for a list of Port entities."""
    entities: List[PortEntity] = field(default_factory=list)
    blueprint_identifier: str = ""
    
    def to_text(self, detailed: bool = False) -> str:
        """
        Returns a textual representation of the entity list.
        
        Args:
            detailed: If True, includes detailed information for each entity.
        """
        if not self.entities:
            return f"No entities found for blueprint '{self.blueprint_identifier}'."
        
        result = f"# Entities for '{self.blueprint_identifier}'\n\n"
        for i, entity in enumerate(self.entities, 1):
            result += f"## {i}. {entity.to_text(detailed=detailed)}\n\n"
        
        return result

@dataclass
class PortAgentResponse:
    """Data model for Port AI agent response."""
    identifier: str
    status: str
    raw_output: Optional[str] = None
    output: Optional[str] = None
    error: Optional[str] = None
    action_url: Optional[str] = None

    def to_text(self) -> str:
        if self.error:
            return f"❌ Error: {self.error}"
        
        if self.status.lower() == "completed":
            response_text = f"✅ Completed!\n\nResponse:\n{self.output}"
            
            # If there's an action URL, add clear instructions
            if self.action_url:
                response_text += "\n\n🔍 Action Required:\n"
                response_text += f"To complete this action, please visit:\n{self.action_url}"
            return response_text
            
        return f"Status: {self.status}\nIdentifier: {self.identifier}"
