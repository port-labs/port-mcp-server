from src.mcp_server_port.client.client import PortClient
from src.mcp_server_port.models.resources.resource import Resource

class GetBlueprints(Resource):
    port_client: PortClient
    def __init__(self, port_client: PortClient):
        super().__init__(name="blueprints", description="Get blueprints summary", uri="blueprints://summary", mimeType="text/plain", function=self.get_blueprints)
        self.port_client = port_client
    def get_blueprints(self) -> str:
        return self.port_client.get_blueprints().to_text(detailed=False)