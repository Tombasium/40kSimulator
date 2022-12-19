from dataclasses import dataclass
from typing import Optional

from model import Model

@dataclass
class Unit():
    name: str
    models: list[Model]

    
