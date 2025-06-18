"""Tests for PortClient custom header functionality."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.client.client import PortClient
from src.utils.user_agent import get_user_agent


@patch('src.client.client.pyport.PortClient')
def test_port_client_sets_user_agent_header(mock_pyport_client):
    """Test that PortClient sets up custom User-Agent header."""
    # Create a mock pyport client instance
    mock_client_instance = Mock()
    mock_pyport_client.return_value = mock_client_instance
    
    # Create our PortClient
    client = PortClient(
        client_id="test_id",
        client_secret="test_secret",
        region="EU"
    )
    
    # Verify pyport client was created
    mock_pyport_client.assert_called_once_with(
        client_id="test_id",
        client_secret="test_secret",
        us_region=False
    )
    
    # Verify that the make_request method was modified to include headers
    assert hasattr(mock_client_instance, 'make_request')
    
    # Test that calling make_request adds the User-Agent header
    mock_original_make_request = Mock()
    mock_client_instance.make_request = mock_original_make_request
    
    # Re-setup headers after setting up the mock
    client._setup_custom_headers()
    
    # Call make_request
    client._client.make_request("GET", "/test")
    
    # Verify the call included User-Agent header
    mock_original_make_request.assert_called_once()
    call_kwargs = mock_original_make_request.call_args[1]
    assert 'headers' in call_kwargs
    assert 'User-Agent' in call_kwargs['headers']
    assert call_kwargs['headers']['User-Agent'] == get_user_agent()


@patch('src.client.client.pyport.PortClient')
def test_port_client_preserves_existing_headers(mock_pyport_client):
    """Test that PortClient preserves existing headers when adding User-Agent."""
    # Create a mock pyport client instance
    mock_client_instance = Mock()
    mock_pyport_client.return_value = mock_client_instance
    
    # Create our PortClient
    client = PortClient(
        client_id="test_id", 
        client_secret="test_secret"
    )
    
    # Mock the original make_request method
    mock_original_make_request = Mock()
    mock_client_instance.make_request = mock_original_make_request
    
    # Re-setup headers
    client._setup_custom_headers()
    
    # Call make_request with existing headers
    existing_headers = {"Authorization": "Bearer token", "Content-Type": "application/json"}
    client._client.make_request("POST", "/test", headers=existing_headers)
    
    # Verify the call preserved existing headers and added User-Agent
    mock_original_make_request.assert_called_once()
    call_kwargs = mock_original_make_request.call_args[1]
    assert 'headers' in call_kwargs
    headers = call_kwargs['headers']
    assert headers['Authorization'] == "Bearer token"
    assert headers['Content-Type'] == "application/json"
    assert headers['User-Agent'] == get_user_agent()


def test_port_client_without_credentials():
    """Test that PortClient handles missing credentials gracefully."""
    client = PortClient()
    
    # Should not have a _client when no credentials are provided
    assert not hasattr(client, '_client') or client._client is None