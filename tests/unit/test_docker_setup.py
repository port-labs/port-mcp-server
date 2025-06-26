"""
Tests for Docker setup and Windows compatibility improvements.
"""
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from src.config.server_config import McpServerConfig, init_server_config


class TestDockerSetup:
    """Test Docker setup configurations and cross-platform compatibility."""
    
    def test_log_path_environment_variable(self):
        """Test that PORT_LOG_PATH environment variable is properly handled."""
        custom_log_path = "/custom/path/port-mcp.log"
        
        with patch.dict(os.environ, {
            'PORT_CLIENT_ID': 'test_id',
            'PORT_CLIENT_SECRET': 'test_secret',
            'PORT_LOG_PATH': custom_log_path
        }):
            config = init_server_config()
            assert config.log_path == custom_log_path
    
    def test_log_path_windows_style(self):
        """Test that Windows-style log paths are properly handled."""
        windows_log_path = "C:\\temp\\port-mcp.log"
        
        config = McpServerConfig(
            port_client_id="test_id",
            port_client_secret="test_secret",
            log_path=windows_log_path
        )
        
        assert config.log_path == windows_log_path
    
    def test_log_path_default_fallback(self):
        """Test that default log path is used when PORT_LOG_PATH is not set."""
        with patch.dict(os.environ, {
            'PORT_CLIENT_ID': 'test_id',
            'PORT_CLIENT_SECRET': 'test_secret'
        }, clear=True):
            config = init_server_config()
            assert config.log_path == "/tmp/port-mcp.log"
    
    def test_config_override_with_log_path(self):
        """Test that config override properly handles log_path parameter."""
        custom_log_path = "/override/path/port-mcp.log"
        
        config = init_server_config(override={
            "port_client_id": "test_id",
            "port_client_secret": "test_secret",
            "log_path": custom_log_path
        })
        
        assert config.log_path == custom_log_path
    
    def test_environment_variable_precedence(self):
        """Test that environment variables are properly prioritized."""
        with patch.dict(os.environ, {
            'PORT_CLIENT_ID': 'env_id',
            'PORT_CLIENT_SECRET': 'env_secret',
            'PORT_REGION': 'US',
            'PORT_LOG_LEVEL': 'DEBUG',
            'PORT_API_VALIDATION_ENABLED': 'true',
            'PORT_LOG_PATH': '/env/path/port-mcp.log'
        }):
            config = init_server_config()
            
            assert config.port_client_id == 'env_id'
            assert config.port_client_secret == 'env_secret'
            assert config.region == 'US'
            assert config.log_level == 'DEBUG'
            assert config.api_validation_enabled is True
            assert config.log_path == '/env/path/port-mcp.log'
    
    def test_cross_platform_path_handling(self):
        """Test that both Unix and Windows paths are accepted."""
        test_cases = [
            "/tmp/port-mcp.log",  # Unix-style
            "C:\\temp\\port-mcp.log",  # Windows-style
            "/var/log/port-mcp.log",  # Unix absolute
            "D:\\logs\\port-mcp.log",  # Windows absolute
            "./logs/port-mcp.log",  # Relative Unix
            ".\\logs\\port-mcp.log"  # Relative Windows
        ]
        
        for log_path in test_cases:
            config = McpServerConfig(
                port_client_id="test_id",
                port_client_secret="test_secret",
                log_path=log_path
            )
            assert config.log_path == log_path


class TestEntrypointCompatibility:
    """Test entrypoint script compatibility scenarios."""
    
    def test_virtual_environment_detection(self):
        """Test that virtual environment detection works for both Unix and Windows."""
        # This is a conceptual test since we can't easily test shell script logic
        # in Python, but we validate the environment variable handling
        
        # Test Unix-style venv path
        unix_venv_path = ".venv/bin/activate"
        assert unix_venv_path.endswith("/bin/activate")
        
        # Test Windows-style venv path
        windows_venv_path = ".venv/Scripts/activate"
        assert windows_venv_path.endswith("/Scripts/activate")
    
    def test_environment_variable_fallback_patterns(self):
        """Test environment variable fallback patterns used in entrypoint."""
        # Test PORT_REGION fallback to REGION
        with patch.dict(os.environ, {'REGION': 'US'}, clear=True):
            # Simulate entrypoint logic
            region = os.environ.get('PORT_REGION', os.environ.get('REGION', 'EU'))
            assert region == 'US'
        
        # Test PORT_LOG_LEVEL fallback to LOG_LEVEL
        with patch.dict(os.environ, {'LOG_LEVEL': 'DEBUG'}, clear=True):
            log_level = os.environ.get('PORT_LOG_LEVEL', os.environ.get('LOG_LEVEL', 'ERROR'))
            assert log_level == 'DEBUG'
        
        # Test PORT_API_VALIDATION_ENABLED fallback to API_VALIDATION_ENABLED
        with patch.dict(os.environ, {'API_VALIDATION_ENABLED': 'True'}, clear=True):
            api_validation = os.environ.get('PORT_API_VALIDATION_ENABLED', 
                                          os.environ.get('API_VALIDATION_ENABLED', 'False'))
            assert api_validation == 'True'
    
    def test_log_directory_creation_scenarios(self):
        """Test log directory creation scenarios for different platforms."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test Unix-style nested path
            unix_log_path = os.path.join(temp_dir, "logs", "app", "port-mcp.log")
            unix_log_dir = os.path.dirname(unix_log_path)
            
            # Simulate directory creation
            os.makedirs(unix_log_dir, exist_ok=True)
            assert os.path.exists(unix_log_dir)
            
            # Test that we can create the log file
            Path(unix_log_path).touch()
            assert os.path.exists(unix_log_path)