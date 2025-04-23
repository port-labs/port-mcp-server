from dataclasses import dataclass
from typing import Callable

@dataclass
class Resource:
    name: str
    description: str
    uri: str
    mimeType: str
    function: Callable
