"""Logging configuration for the Port MCP server."""

from __future__ import annotations

import sys

import loguru


def setup_basic_logging():
    """Set up basic logging without config dependency."""
    # Remove default logger
    loguru.logger.remove()
    # Add stdout handler with basic settings
    loguru.logger.add(
        sys.stdout,
        format="""
<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> |
    <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>""",
        level="INFO",
        colorize=True,
    )
    return loguru.logger


def setup_logging_with_config(config):
    """Set up logging with config-specific settings."""
    # Remove existing handlers
    loguru.logger.remove()
    # Add handler with config settings
    loguru.logger.add(
        config.log_path if config.log_path else sys.stdout,
        format="""
<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> |
    <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>""",
        level=config.log_level,
        colorize=True,
    )
    loguru.logger.info("Logging configured with loguru")
    loguru.logger.debug(f"Config: {config}")
    return loguru.logger


# Initialize basic logger immediately to avoid circular dependency
logger: loguru.Logger = setup_basic_logging()


def get_logger() -> loguru.Logger:
    """Get the global logger."""
    return logger


def update_logger_with_config(config):
    """Update the logger with config settings."""
    global logger
    logger = setup_logging_with_config(config)
