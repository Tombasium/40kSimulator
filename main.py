from combat import attack

from utils import *

from simulate import run_simulation

from unit import Unit

from control import run, run_shooting_sim

from statistics import mean

from shooting_utils import parse_unit_shooting_data

from shooting_sim import make_shooting_attack


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

#print(weapon_profile)
#for x in unit_profile["Weapons"]:
    # print(x)

#print(parse_unit_shooting_data()["Kasrkin"]["Model count"])


# dice = "2D6+2".split("+")

# print(dice)


#make_shooting_attack('Field Ordnance Malleus', 'Skitarii Vanguard', born_soldiers_trigger=5, half_range=True)


#make_shooting_attack('Mortars', 'Skitarii Vanguard', born_soldiers_trigger=5, half_range=True)

make_shooting_attack('Kasrkin', 'Skitarii Vanguard', born_soldiers_trigger=5, half_range=True)


# wounds_caused = [1, 1, 1, 1, 2, 2, 3]
# defender_wounds = [2, 2, 3, 3, 3]

# print("{0} defenders are struck by {1} attacks!\n".format(len(defender_wounds), len(wounds_caused)))

# while len(defender_wounds) > 0 and len(wounds_caused) > 0:
#     defender_wounds = sorted(defender_wounds)
#     for defender in defender_wounds:
#         if defender in wounds_caused:
#             defender_wounds.remove(defender)
#             wounds_caused.remove(defender)
# #            print("attack killed one defender: {0} defenders and {1} hits remain".format(len(defender_wounds), len(wounds_caused)))
#             break
#         elif max(wounds_caused) < defender:
#             print(defender_wounds)
#             highest_damage = max(wounds_caused)
#             defender_wounds.remove(defender)
#             defender_wounds.append(defender - highest_damage)
#             wounds_caused.remove(highest_damage)
#             print(defender_wounds)
# #            print("Attack takes {0} wounds from defender, which has {1} wounds remaining. {2} wounds remain to be resolved".format(highest_damage, defender, len(wounds_caused)))
#             break
#         elif min(wounds_caused) > defender:
#             print(defender_wounds)
#             lowest_damage = min(wounds_caused)
#             defender_wounds.remove(defender)
#             defender_wounds.append(defender - lowest_damage)
#             wounds_caused.remove(lowest_damage)
#             print(defender_wounds)
#            print("Attack takes {0} wounds from defender on {1} wounds; {2} defenders and {3} hits remain".format(lowest_damage, defender, len(defender_wounds), len(wounds_caused)))
            # break
# print("\n{0} defenders and {1} attacks remain!".format(len(defender_wounds), len(wounds_caused)))
