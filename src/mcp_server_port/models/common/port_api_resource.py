"""Base class for Port.io API resources."""

from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class PortApiResource:
    """
    Base class for all Port.io API resources.
    
    This class provides common functionality for all resources
    that can be created, retrieved, updated, or deleted through
    the Port.io API.
    """
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the resource to a dictionary for API requests.
        
        This method should be implemented by all subclasses.
        """
        raise NotImplementedError("Subclasses must implement to_dict") 