from dataclasses import dataclass
from typing import Optional

from weapon import Weapon

from utils import parse_model_data

MODELS = parse_model_data()

@dataclass
class Model():
    name: str
    stats: dict
    weapons: list[Weapon]
    
    def __init__(self, modelName: str):
        self.name = modelName
        self.stats = MODELS[modelName]
        self.weapons = self.stats.get("Weapons")
