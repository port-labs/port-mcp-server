#!/usr/bin/env python3
"""
Simple integration test to validate the User-Agent header setup.
This doesn't require external dependencies.
"""

import sys
import os
sys.path.append('src')

# Mock pyport to test our header injection
class MockPortClient:
    def __init__(self, **kwargs):
        self.make_request_calls = []
        
    def make_request(self, method, endpoint, **kwargs):
        self.make_request_calls.append({
            'method': method,
            'endpoint': endpoint,
            'kwargs': kwargs
        })
        # Mock response
        class MockResponse:
            def json(self):
                return {"ok": True, "data": "test"}
        return MockResponse()

# Mock pyport module
class MockPyportModule:
    PortClient = MockPortClient

# Inject mock
sys.modules['pyport'] = MockPyportModule()

# Now we can import our client
from src.client.client import PortClient

def test_user_agent_header():
    """Test that User-Agent header is properly set."""
    # Set up environment for testing
    os.environ['PORT_CLIENT_ID'] = 'test_id'
    os.environ['PORT_CLIENT_SECRET'] = 'test_secret'
    os.environ['PORT_MCP_CLIENT'] = 'vscode'
    
    # Create PortClient
    client = PortClient(
        client_id='test_id',
        client_secret='test_secret'
    )
    
    # Make a test request
    client._client.make_request('GET', '/test/endpoint')
    
    # Check that the call was made with User-Agent header
    calls = client._client.make_request_calls
    assert len(calls) == 1
    
    call = calls[0]
    headers = call['kwargs'].get('headers', {})
    user_agent = headers.get('User-Agent', '')
    
    print(f"User-Agent header: {user_agent}")
    
    # Validate format
    assert user_agent.startswith('port-mcp-server/')
    parts = user_agent.split('/')
    assert len(parts) == 3
    assert parts[0] == 'port-mcp-server'
    assert parts[1]  # Should have MCP client
    assert parts[2]  # Should have version
    
    print("✓ User-Agent header validation passed")

def test_header_preservation():
    """Test that existing headers are preserved."""
    os.environ['PORT_CLIENT_ID'] = 'test_id'
    os.environ['PORT_CLIENT_SECRET'] = 'test_secret'
    
    client = PortClient(
        client_id='test_id',
        client_secret='test_secret'
    )
    
    # Make request with existing headers
    existing_headers = {
        'Authorization': 'Bearer token',
        'Content-Type': 'application/json'
    }
    client._client.make_request('POST', '/test', headers=existing_headers)
    
    # Check headers were preserved and User-Agent was added
    calls = client._client.make_request_calls
    call = calls[-1]  # Get the last call
    headers = call['kwargs']['headers']
    
    assert headers['Authorization'] == 'Bearer token'
    assert headers['Content-Type'] == 'application/json'
    assert 'User-Agent' in headers
    assert headers['User-Agent'].startswith('port-mcp-server/')
    
    print("✓ Header preservation test passed")

if __name__ == '__main__':
    test_user_agent_header()
    test_header_preservation()
    print("All tests passed!")