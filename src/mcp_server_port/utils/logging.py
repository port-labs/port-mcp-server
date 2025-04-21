"""Logging configuration for the Port MCP server."""

import sys
import logging
from loguru import logger

# Intercept standard library logging
class InterceptHandler(logging.Handler):
    """Intercept standard library logging and redirect to loguru."""
    
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        
        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def setup_logging(level="INFO"):
    """
    Configure loguru logging.
    
    Args:
        level: Minimum log level to display (default: INFO)
    """
    # Remove default logger
    logger.remove()
    
    # Add stdout handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level,
        colorize=True
    )
    
    # Add file handler for errors and above
    logger.add(
        "logs/error.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        rotation="10 MB",
        retention="1 week"
    )
    
    # Add file handler for all logs
    logger.add(
        "logs/port_mcp.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=level,
        rotation="10 MB",
        retention="3 days"
    )
    
    # Intercept standard library logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    
    # List of loggers to configure
    loggers = [
        logging.getLogger(name) 
        for name in logging.root.manager.loggerDict
        if name.startswith("mcp_server_port")
    ]
    
    # Also configure root logger
    loggers.append(logging.getLogger())
    
    # Configure all loggers
    for log in loggers:
        log.handlers = [InterceptHandler()]
        log.propagate = False
        log.level = 0
        
    logger.info("Logging configured with loguru")
    
    return logger 