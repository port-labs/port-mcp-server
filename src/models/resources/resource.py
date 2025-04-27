from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Resource:
    name: str
    description: str
    uri: str
    mime_type: str
    function: Callable
