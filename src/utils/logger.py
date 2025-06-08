"""Logging configuration for the Port MCP server."""

from __future__ import annotations

import sys

import loguru

from src.config import config


def setup_logging():
    # Remove default logger
    loguru.logger.remove()
    # Add stdout handler
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


logger: loguru.Logger = setup_logging()
