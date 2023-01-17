from combat import attack

from utils import *

from simulate import run_simulation

from unit import Unit

from control import run, run_shooting_sim

from statistics import mean

from shooting_utils import parse_unit_shooting_data


def getAttackProfile(attacker: Unit, defender: Unit, waagh = False):
    attacker.getAttackProfile()
    defender.getDefendProfile()
    attackProfile = {
        'attacker': attacker.name,
        'defender': defender.name,
        'waagh': waagh,
        'profile':{
            **attacker.attackProfile,
            **defender.defenceProfile
        }
    }

def fight(
    attacker: Unit, 
    defender: Unit, 
    numAttackers: int, 
    numDefenders: int,
    waagh: bool
    ):
    getAttackProfile(attacker, defender, waagh)

# # run(defender = 'Tyranid Warriors')

input = {
    "iterations":  10000, 
    "take_aim": False, 
    "ingrained_precision": True,
    "half_range": True,
    "FRFSRF":  True,
    "Leontus": True,
    "Leontus_balls": True,
    "regimental_standard": False,
    "castellan": False,
    "overcharged_las": True
}

#run_shooting_sim(**input)

profiles = parse_unit_shooting_data()

unit_profile = profiles["Kasrkin"]

weapon_profile = unit_profile["Weapons"]["Hotshot Volleygun"]

print(weapon_profile)
#for x in unit_profile["Weapons"]:
    # print(x)

print(parse_unit_shooting_data()["Kasrkin"]["Model count"])


# dice = "2D6+2".split("+")

# print(dice)
