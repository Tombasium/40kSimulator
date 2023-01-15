from dataclasses import dataclass
from typing import Optional

from model import Model

from utils import parse_unit_data

UNITS = parse_unit_data()

    # "Nobz": {
    #     "Nob": {
    #         "min": 4,
    #         "max": 9
    #     },
    #     "BossNob": {
    #         "leader": true,
    #         "min": 1,
    #         "max": 1
    #     }
    # },

@dataclass
class Unit():
    name: str
    models: list[Model]

    def __init__(self, unitType: str, number: int):
        self.name = unitType
        template = UNITS[unitType]
        for i in template.items():
            if 'leader' in i[1].keys():
                leader = Model(i[0])
            else:
                troop = Model(i[0])
        self.models = [leader, [troop for x in range((number -1))]]

    
