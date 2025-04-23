"""Logging configuration for the Port MCP server."""

import sys
from loguru import logger
import src.server.config.config as server_config 

def setup_logging():
    # Remove default logger
    logger.remove()
    # Add stdout handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=server_config.config.log_level,
        colorize=True
    )
    print(f"log level: {server_config.config.log_level}")
    logger.info("Logging configured with loguru")
    
    return logger