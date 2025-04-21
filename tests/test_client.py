import pytest
import sys
from unittest.mock import AsyncMock, MagicMock, patch
import requests

# Add src to path
sys.path.append('src')

from src.mcp_server_port.client.client import PortClient
from src.mcp_server_port.utils import PortError


@pytest.fixture
def mock_pyport_client():
    """Create a mock PyPort client."""
    return MagicMock()


@pytest.fixture
def port_client(mock_pyport_client):
    """Create a PortClient with a mocked PyPort client."""
    with patch('src.mcp_server_port.client.client.pyport.PortClient', return_value=mock_pyport_client):
        client = PortClient(client_id="test_id", client_secret="test_secret")
        return client


@pytest.mark.asyncio
async def test_port_client_initialization():
    """Test that PortClient initializes correctly."""
    # Test with credentials
    with patch('src.mcp_server_port.client.client.pyport.PortClient') as mock_pyport:
        client = PortClient(client_id="test_id", client_secret="test_secret")
        mock_pyport.assert_called_once_with(
            client_id="test_id", 
            client_secret="test_secret", 
            us_region=False
        )
        assert client._client is not None
        assert client.agent is not None
        assert client.blueprints is not None
        assert client.entities is not None
        assert client.scorecards is not None

    # Test with US region
    with patch('src.mcp_server_port.client.client.pyport.PortClient') as mock_pyport:
        client = PortClient(client_id="test_id", client_secret="test_secret", region="US")
        mock_pyport.assert_called_once_with(
            client_id="test_id", 
            client_secret="test_secret", 
            us_region=True
        )

    # Test without credentials
    client = PortClient()
    assert client._client is None
    assert client.agent is None
    assert client.blueprints is None
    assert client.entities is None
    assert client.scorecards is None


@pytest.mark.asyncio
async def test_handle_http_error(port_client):
    """Test that HTTP errors are handled correctly."""
    # Mock a requests.exceptions.HTTPError
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.json.return_value = {"error": "Forbidden"}
    
    mock_request = MagicMock()
    mock_request.method = "GET"
    mock_request.url = "https://api.example.com/test"
    
    mock_error = requests.exceptions.HTTPError()
    mock_error.response = mock_response
    mock_error.request = mock_request
    
    # Test that handle_http_error raises a PortError
    with pytest.raises(PortError) as excinfo:
        port_client.handle_http_error(mock_error)
    
    assert "Error in GET https://api.example.com/test - 403" in str(excinfo.value)


@pytest.mark.asyncio
async def test_wrap_request_success(port_client):
    """Test that wrap_request returns the result of the request if successful."""
    async def mock_request():
        return {"success": True}
    
    result = await port_client.wrap_request(mock_request)
    assert result == {"success": True}


@pytest.mark.asyncio
async def test_wrap_request_http_error(port_client):
    """Test that wrap_request handles HTTP errors correctly."""
    # Mock a requests.exceptions.HTTPError
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"error": "Not Found"}
    
    mock_request = MagicMock()
    mock_request.method = "GET"
    mock_request.url = "https://api.example.com/test"
    
    mock_error = requests.exceptions.HTTPError()
    mock_error.response = mock_response
    mock_error.request = mock_request
    
    async def mock_request():
        raise mock_error
    
    # Test that wrap_request raises a PortError
    with pytest.raises(PortError):
        await port_client.wrap_request(mock_request)


@pytest.mark.asyncio
async def test_client_methods(port_client, mock_pyport_client):
    """Test that client methods call the corresponding methods on the client components."""
    # Setup mock returns
    mock_pyport_client.agent.trigger_agent = AsyncMock(return_value={"invocation_id": "123"})
    mock_pyport_client.agent.get_invocation_status = AsyncMock(return_value={"status": "completed"})
    mock_pyport_client.blueprints.get_blueprints = AsyncMock(return_value=[{"id": "test"}])
    mock_pyport_client.blueprints.get_blueprint = AsyncMock(return_value={"id": "test"})
    mock_pyport_client.entities.get_entities = AsyncMock(return_value=[{"id": "test"}])
    mock_pyport_client.entities.get_entity = AsyncMock(return_value={"id": "test"})
    
    # Test client methods
    result = await port_client.trigger_agent("test prompt")
    mock_pyport_client.agent.trigger_agent.assert_awaited_once_with("test prompt")
    assert result == {"invocation_id": "123"}
    
    result = await port_client.get_invocation_status("123")
    mock_pyport_client.agent.get_invocation_status.assert_awaited_once_with("123")
    assert result == {"status": "completed"}
    
    result = await port_client.get_blueprints()
    mock_pyport_client.blueprints.get_blueprints.assert_awaited_once()
    assert result == [{"id": "test"}]
    
    result = await port_client.get_blueprint("test")
    mock_pyport_client.blueprints.get_blueprint.assert_awaited_once_with("test")
    assert result == {"id": "test"}
    
    result = await port_client.get_entities("test")
    mock_pyport_client.entities.get_entities.assert_awaited_once_with("test")
    assert result == [{"id": "test"}]
    
    result = await port_client.get_entity("test", "test-entity")
    mock_pyport_client.entities.get_entity.assert_awaited_once_with("test", "test-entity")
    assert result == {"id": "test"} 