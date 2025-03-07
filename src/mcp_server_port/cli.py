"""
Command-line interface for the Port.io MCP Server.
"""

import argparse
from .server import main

def parse_args():
    """Parse command-line arguments for the Port.io MCP Server."""
    parser = argparse.ArgumentParser(description="Port.io MCP Server")
    parser.add_argument("--client-id", help="Port.io Client ID", required=True)
    parser.add_argument("--client-secret", help="Port.io Client Secret", required=True)
    parser.add_argument("--region", default="EU", help="Port.io API region (EU or US)")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    
    return parser.parse_args()

def cli_main():
    """
    Command-line entry point for the package.
    This is the main entry point for all command-line executions.
    """
    # Parse command-line arguments
    args = parse_args()
    
    # Call the main function with command-line arguments
    main(
        client_id=args.client_id,
        client_secret=args.client_secret,
        region=args.region,
        debug=args.debug
    )

if __name__ == "__main__":
    cli_main()
