"""
Entry point for the Port.io MCP server.
"""

from .cli import cli_main

if __name__ == "__main__":
    print("Starting CLI...")
    cli_main()
