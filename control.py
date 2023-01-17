from simulate import run_simulation

from attackProfiles import attack_profiles

from utils import generate_result_string, make_word_green

from shooting_sim import shock_troops_into_vanguard, tempestus_into_vanguard, kasrkin_into_vanguard

from statistics import mean

def run(defender: str, attacker: str = None, iterations: int = 10000):
    for profile in attack_profiles:
        if (profile['defender'] == defender and (profile['attacker'] == attacker or attacker is None)):
            result = run_simulation(iterations, profile['profile'])
            print(generate_result_string(
                profile['attacker'],
                profile['defender'],
                profile['waagh'],
                result
            ))

def run_shooting_sim(
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
        "BS": shock_bs,
        "born_soldiers_trigger": born_soldiers_trigger,
        "half_range": half_range,
        "FRFSRF": FRFSRF,
        "Leontus": Leontus,
        "regimental_standard": regimental_standard,
        "castellan": castellan
    }

    tempestus_input = {
        "BS": tempestus_bs,
        "half_range": half_range,
        "FRFSRF": FRFSRF,
        "Leontus": Leontus,
        "Leontus_balls": Leontus_balls,
        "regimental_standard": regimental_standard,
        "castellan": castellan,
        "overcharged_las": overcharged_las
    }

    kasrkin_input = {
        "BS": tempestus_bs,
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
