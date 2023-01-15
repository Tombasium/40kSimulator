from dataclasses import dataclass
from typing import Optional

from utils import parse_weapon_data

WEAPONS = parse_weapon_data()

@dataclass
class Weapon():
    name: str
    stats: dict
    abilities: Optional[list]

    def __init__(self, weapon_name: str):
        self.name = weapon_name,
        self.stats = WEAPONS[weapon_name]['stats']
        self.abilities = self.stats.get('Abilities')
    
    
