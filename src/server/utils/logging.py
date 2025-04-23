"""Logging configuration for the Port MCP server."""

import sys
from loguru import logger
from src.server.config import config

def setup_logging(level="INFO"):
    # Remove default logger
    logger.remove()
    # Add stdout handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level,
        colorize=True
    )
    logger.level(config.log_level)
    
    logger.info("Logging configured with loguru")
    
    return logger