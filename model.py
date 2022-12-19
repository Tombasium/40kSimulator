from dataclasses import dataclass
from typing import Optional

from weapon import Weapon

@dataclass
class Model():
    name: str
    M: int
    WS: int
    BS: int
    S: int
    T: int
    W: int
    A: int
    Ld: int
    Sv: int
    base: int
    inv: Optional[int]
    HRAmod: Optional[int]
    HRDmod: Optional[int]
    WRAmod: Optional[int]
    WRDmod: Optional[int]
    Weapons: Optional[list[Weapon]]
    Abilities: Optional[list]
    
