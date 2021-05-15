from dataclasses import dataclass
from typing import Set, List

from .author import Author


@dataclass
class Track:
    id: int
    checksum: str
    links: Set[str]
    authors: List[Author]
