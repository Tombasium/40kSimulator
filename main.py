from combat import attack

from utils import *

from simulate import run_simulation

from unit import Unit

from control import run

from statistics import mean

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

# run(defender = 'Tyranid Warriors')

def shock_troops_into_vanguard(
    bs: int = 4, 
    born_soldiers_trigger: int = 6, 
    half_range: bool = False, 
    FRFSRF: bool = False,
    Leontus: bool = False,
    Leontus_balls: bool = False,
    regimental_standard: bool = False,
    castellan: bool = False
    ):

    las_shots = 7
    plasma_shots = 2
    autogun_shots = 2

    if half_range:
        las_shots = 14
        plasma_shots = 4
        autogun_shots = 4
    
    if FRFSRF:
        las_shots = 21

    las_attacks = [roll_d6() for x in range(las_shots)]
    plasma_attacks = [roll_d6() for x in range(plasma_shots)]
    autogun_attacks = [roll_d6() for x in range(autogun_shots)]

    las_wounds = [roll_d6() for x in las_attacks if x >= bs] + [6 for x in las_attacks if x >= born_soldiers_trigger]
    plas_wounds = [roll_d6() for x in plasma_attacks if x >= bs and x < born_soldiers_trigger] + [6 for x in plasma_attacks if x >= born_soldiers_trigger]
    autogun_wounds = [roll_d6() for x in autogun_attacks if x >= bs and x < born_soldiers_trigger] + [6 for x in autogun_attacks if x >= born_soldiers_trigger]

    las_saves = [roll_d6() for x in las_wounds if x >= 4]
    plas_saves = [roll_d6() for x in plas_wounds if x >= 2]
    autogun_saves = [roll_d6() for x in autogun_wounds if x >= 4]

    wounds = len([x for x in las_saves if x < 4] + [x for x in plas_saves if x < 5] + [x for x in autogun_saves if x < 4])

    return wounds

def tempestus_into_vanguard(
    bs: int = 3,
    half_range: bool = False, 
    FRFSRF: bool = False,
    Leontus: bool = False,
    Leontus_balls: bool = False,
    regimental_standard: bool = False,
    castellan: bool = False,
    overcharged_las: bool = False
    ):

    las_shots = 6
    plasma_shots = 2
    las_volley_shots = 4

    if half_range:
        las_shots = 11
        plasma_shots = 4
        las_volley_shots = 8
    
    if FRFSRF:
        las_shots = 16

    las_attacks = [roll_d6() for x in range(las_shots)]
    plasma_attacks = [roll_d6() for x in range(plasma_shots)]
    las_volley_attacks = [roll_d6() for x in range(las_volley_shots)]

    las_wounds = [roll_d6() for x in las_attacks if x >= bs] + [roll_d6() for x in las_attacks if x == 6]
    plas_wounds = [roll_d6() for x in plasma_attacks if x >= bs] + [roll_d6() for x in plasma_attacks if x == 6]
    las_volley_wounds = [roll_d6() for x in las_volley_attacks if x >= bs] + [roll_d6() for x in las_volley_attacks if x == 6]

    las_saves = [roll_d6() for x in las_wounds if x >= 4]
    plas_saves = [roll_d6() for x in plas_wounds if x >= 2]
    las_volley_saves = [roll_d6() for x in las_volley_wounds if x >= 3]

    wounds = len([x for x in las_saves if x < 5] + [x for x in plas_saves if x < 5] + [x for x in las_volley_saves if x < 5])

    return wounds

def kasrkin_into_vanguard(
    bs: int = 3, 
    born_soldiers_trigger: int = 6, 
    half_range: bool = False, 
    FRFSRF: bool = False,
    Leontus: bool = False,
    Leontus_balls: bool = False,
    regimental_standard: bool = False,
    castellan: bool = False,
    overcharged_las: bool = False
    ):

    las_shots = 6
    plasma_shots = 2
    las_volley_shots = 4

    if half_range:
        las_shots = 11
        plasma_shots = 4
        las_volley_shots = 8
    
    if FRFSRF:
        las_shots = 16


    las_attacks = [roll_d6() for x in range(las_shots)]
    plasma_attacks = [roll_d6() for x in range(plasma_shots)]
    las_volley_attacks = [roll_d6() for x in range(las_volley_shots)]

    if Leontus_balls:
        las_attacks_balls = [x for x in las_attacks if x >= born_soldiers_trigger] + [roll_d6() for x in las_attacks if x < born_soldiers_trigger]
        las_attacks = las_attacks_balls

        plasma_attacks_balls = [x for x in plasma_attacks if x >= born_soldiers_trigger] + [roll_d6() for x in plasma_attacks if x < born_soldiers_trigger]
        plasma_attacks = plasma_attacks_balls

        las_volley_attacks_balls = [x for x in las_volley_attacks if x >= born_soldiers_trigger] + [roll_d6() for x in las_volley_attacks if x < born_soldiers_trigger]
        las_volley_attacks = las_volley_attacks_balls

    elif Leontus:
        las_attacks_leontus = [x for x in las_attacks if x >= bs] + [roll_d6() for x in las_attacks if x < bs]
        las_attacks = las_attacks_leontus

        plasma_attacks_leontus = [x for x in plasma_attacks if x >= bs] + [roll_d6() for x in plasma_attacks if x < bs]
        plasma_attacks = plasma_attacks_leontus

        las_volley_attacks_leontus = [x for x in las_volley_attacks if x >= bs] + [roll_d6() for x in las_volley_attacks if x < bs]
        las_volley_attacks = las_volley_attacks_leontus

    elif castellan:
        las_attacks_castellan = [x for x in las_attacks if x > 1] + [roll_d6() for x in las_attacks if x == 1]
        las_attacks = las_attacks_castellan

    las_wounds = [roll_d6() for x in las_attacks if x >= bs] + [6 for x in las_attacks if x >= born_soldiers_trigger]
    plas_wounds = [roll_d6() for x in plasma_attacks if x >= bs and x < born_soldiers_trigger] + [6 for x in plasma_attacks if x >= born_soldiers_trigger]
    las_volley_wounds = [roll_d6() for x in las_volley_attacks if x >= bs and x < born_soldiers_trigger] + [6 for x in las_volley_attacks if x >= born_soldiers_trigger]

    number_of_sixes = len([x for x in las_wounds if x == 6] + [x for x in plas_wounds if x == 6] + [x for x in las_volley_wounds if x == 6])

    if Leontus_balls and overcharged_las and number_of_sixes < 6:
        las_wounds_balls = [roll_d6() for x in las_wounds if x < 6] + [x for x in las_wounds if x == 6]
        las_wounds = las_wounds_balls

        plas_wounds_balls = [roll_d6() for x in plas_wounds if x < 6] + [x for x in plas_wounds if x == 6]
        plas_wounds = plas_wounds_balls

        las_volley_wounds_balls = [roll_d6() for x in las_volley_wounds if x < 6] + [x for x in las_volley_wounds if x == 6]
        las_volley_wounds = las_volley_wounds_balls
    
    elif Leontus:
        las_wounds_leontus = [roll_d6() for x in las_wounds if x < 4] + [x for x in las_wounds if x >= 4]
        las_wounds = las_wounds_leontus

        plas_wounds_leontus = [roll_d6() for x in plas_wounds if x < 2] + [x for x in plas_wounds if x >= 2]
        plas_wounds = plas_wounds_leontus

        las_volley_wounds_leontus = [roll_d6() for x in las_volley_wounds if x < 3] + [x for x in las_volley_wounds if x >= 3]
        las_volley_wounds = las_volley_wounds_leontus
    
    elif regimental_standard:
        las_wounds_leontus = [roll_d6() for x in las_wounds if x == 1] + [x for x in las_wounds if x >= 1]
        las_wounds = las_wounds_leontus

        plas_wounds_leontus = [roll_d6() for x in plas_wounds if x == 1] + [x for x in plas_wounds if x >= 1]
        plas_wounds = plas_wounds_leontus

        las_volley_wounds_leontus = [roll_d6() for x in las_volley_wounds if x == 1] + [x for x in las_volley_wounds if x >= 1]
        las_volley_wounds = las_volley_wounds_leontus

    number_of_sixes = len([x for x in las_wounds if x == 6] + [x for x in plas_wounds if x == 6] + [x for x in las_volley_wounds if x == 6])

    las_saves = [roll_d6() for x in las_wounds if x >= 4]
    plas_saves = [roll_d6() for x in plas_wounds if x >= 2]
    las_volley_saves = [roll_d6() for x in las_volley_wounds if x >= 4]

    wounds = len([x for x in las_saves if x < 5] + [x for x in plas_saves if x < 5] + [x for x in las_volley_saves if x < 5])
    
    if overcharged_las:
        wounds += min(6, number_of_sixes)

    return wounds


def run_sim(
    iterations: int = 10000, 
    take_aim: bool = False, 
    ingrained_precision: bool = False,
    half_range: bool = False,
    FRFSRF: bool = False,
    Leontus: bool = False,
    Leontus_balls: bool = False,
    regimental_standard: bool = False,
    castellan: bool = False,
    overcharged_las: bool = False
    ):

    shock_bs = 4
    tempestus_bs = 3
    kasrkin_bs = 3
    if take_aim:
        shock_bs -= 1
        tempestus_bs -= 1
        kasrkin_bs -= 1

    born_soldiers_trigger = 6
    if ingrained_precision:
        born_soldiers_trigger -= 1

    shock_input = {
        "bs": shock_bs,
        "born_soldiers_trigger": born_soldiers_trigger,
        "half_range": half_range,
        "FRFSRF": FRFSRF,
        "Leontus": Leontus,
        "Leontus_balls": Leontus_balls,
        "regimental_standard": regimental_standard,
        "castellan": castellan
    }

    tempestus_input = {
        "bs": tempestus_bs,
        "half_range": half_range,
        "FRFSRF": FRFSRF,
        "Leontus": Leontus,
        "Leontus_balls": Leontus_balls,
        "regimental_standard": regimental_standard,
        "castellan": castellan,
        "overcharged_las": overcharged_las
    }

    kasrkin_input = {
        "bs": tempestus_bs,
        "born_soldiers_trigger": born_soldiers_trigger,
        "half_range": half_range,
        "FRFSRF": FRFSRF,
        "Leontus": Leontus,
        "Leontus_balls": Leontus_balls,
        "regimental_standard": regimental_standard,
        "castellan": castellan,
        "overcharged_las": overcharged_las
    }
    
    shock_results = [shock_troops_into_vanguard(**shock_input) for x in range(iterations)]
    tempestus_results = [tempestus_into_vanguard(**tempestus_input) for x in range(iterations)]
    kasrkin_results = [kasrkin_into_vanguard(**kasrkin_input) for x in range(iterations)]

    print('Shock troopers do {0} wounds on average'.format(make_word_green(mean(shock_results))))
    print('Tempestus do {0} wounds on average'.format(make_word_green(mean(tempestus_results))))
    print('Kasrkin do {0} wounds on average'.format(make_word_green(mean(kasrkin_results))))

run_sim(take_aim = True, ingrained_precision=False, overcharged_las=False, half_range=True, FRFSRF=True)
