from dataclasses import dataclass
from typing import Set, List

from .author import Author


@dataclass
class Track:
    id: int
    title: str
    checksum: str
    links: Set[str]
    authors: List[Author]
