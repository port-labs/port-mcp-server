"""
Command-line interface for the Port.io MCP Server.
"""

import argparse

from src import main
from src.config.server_config import McpServerConfig, init_server_config


def parse_args():
    """Parse command-line arguments for the Port.io MCP Server."""
    parser = argparse.ArgumentParser(description="Port.io MCP Server")
    parser.add_argument("--client-id", help="Port.io Client ID", required=True)
    parser.add_argument("--client-secret", help="Port.io Client Secret", required=True)
    parser.add_argument("--region", default="EU", help="Port.io API region (EU or US)")
    parser.add_argument("--log-level", default="ERROR", help="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    parser.add_argument("--api-validation-enabled", default="False", help="Enable API validation")

    return parser.parse_args()


def cli_main():
    """
    Command-line entry point for the package.
    This is the main entry point for all command-line executions.
    """
    # Parse command-line arguments
    args = parse_args()
    init_server_config(
        McpServerConfig(
            port_client_id=args.client_id,
            port_client_secret=args.client_secret,
            region=args.region,
            log_level=args.log_level,
            api_validation_enabled=args.api_validation_enabled.lower() == "true",
        ).model_dump()
    )
    # Call the main function with command-line arguments
    main()


if __name__ == "__main__":
    cli_main()
