from dataclasses import dataclass
from typing import Optional

@dataclass
class Weapon():
    name: str
    range: int
    type: str
    S: Optional[int]
    AP: int
    D: int 
    Abilities: Optional[list]

    