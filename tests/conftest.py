"""Configuration file for pytest."""
import os
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

# Set default asyncio fixture scope
pytest_plugins = ["pytest_asyncio"]

# Add the src directory to the path so we can import our modules
# Using absolute path for reliability
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path) 