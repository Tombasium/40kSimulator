from utils import *

from combat import determine_wound_roll_needed

from typing import Optional

from shooting_utils import parse_unit_shooting_data

def apply_born_soldiers(
    shots = list[int]
):
    pass

def apply_rerolls(
    rolls: list[int],
    reroll_under: int
):
    return [x for x in rolls if x >= reroll_under] + [roll_d6() for x in rolls if x < reroll_under]

def apply_overcharged_las(
    shots: list[int]
):
    return min(6, shots.count(6))

def apply_leontus_rerolls(
    rolls: list[int],
    BS: int
):
    return apply_rerolls(rolls=rolls, reroll_under=BS)

def apply_leontus_ballsy_rerolls(
    rolls: list[int],
    born_soldiers_trigger: int
):
    return apply_rerolls(rolls=rolls, reroll_under=born_soldiers_trigger)
    
def apply_reroll_ones(
    rolls: list[int]
):
    return apply_rerolls(rolls=rolls, reroll_under=2)

def get_hit_rolls(
    shots: int,
    BS: int,
    castellan: bool = False,
    leontus: bool = False,
    leontus_ballsy_hit: bool = False,
    born_soldiers_trigger: Optional[int] = None,
    hit_roll_positive_modifier: int = 0,
    hit_roll_negative_modifier: int = 0
):
    hit_rolls = [roll_d6() for x in range(shots)]
    
    hit_roll_needed = min(max(BS - hit_roll_positive_modifier + hit_roll_negative_modifier, 2), 6)

    if leontus_ballsy_hit:
        hit_rolls = apply_leontus_ballsy_rerolls(hit_rolls, born_soldiers_trigger)
    elif leontus:
        hit_rolls = apply_leontus_rerolls(hit_rolls, hit_roll_needed)
    elif castellan:
        hit_rolls = apply_reroll_ones(hit_rolls)

    if born_soldiers_trigger:
        modified_hit_rolls = [x for x in hit_rolls if x >= BS and x < born_soldiers_trigger] + [6 for x in hit_rolls if x >= born_soldiers_trigger]
        hit_rolls = modified_hit_rolls

    return hit_rolls


def get_wound_rolls(
    hits: list[int],
    S: int,
    T: int,
    BS: int,
    leontus_ballsy_wound: bool = False,
    leontus: bool = False,
    regimental_standard: bool = False,
    overcharged_las: bool = False,
    born_soldiers_trigger: Optional[int] = None
):
    needed = determine_wound_roll_needed(S=S, T=T)

    if born_soldiers_trigger:
        rolls = [roll_d6() for x in hits if x < born_soldiers_trigger] + [6 for x in hits if x >= born_soldiers_trigger]
    else: 
        rolls = [roll_d6() for x in hits]
    
    if leontus_ballsy_wound:
        rolls = apply_leontus_ballsy_rerolls(rolls=rolls, born_soldiers_trigger=born_soldiers_trigger)
    elif leontus:
        rolls = apply_leontus_rerolls(rolls=rolls, BS=BS)
    elif regimental_standard: 
        rolls = apply_reroll_ones(rolls=rolls)
    
    return [x for x in rolls if x >= needed]

def roll_variable_dice(
    dice: str,
    size_of_target_unit: int, 
    blast: bool = False
):
    result = 0

    components = result.split("+")

    if len(components > 1):
        result = int(components[1])
    
    dice_to_roll_components = components.split("D")

    if len(dice_to_roll_components > 1):
        if dice_to_roll_components[1] == "3":
            for x in range(int(dice_to_roll_components[0])):
                result += roll_d3()
                max_shots = int(dice_to_roll_components[0]) * 3

        if dice_to_roll_components[1] == "6":
            for x in range(int(dice_to_roll_components[0])):
                result += roll_d6()
                max_shots = int(dice_to_roll_components[0]) * 6

    if blast:
        if size_of_target_unit >= 6 and size_of_target_unit < 11:
            result = max(result, 3)
        elif size_of_target_unit >= 11:
            result = max_shots
    
    return result

def determine_number_of_shots(
    weapon: dict,
    target_unit_size: int,
    half_range: bool = False
):
    number_of_weapons = weapon["Number"]

    type = weapon["Type"]

    shots_per_weapon = weapon["Shots"]

    blast = weapon.get("Blast", False)

    if isinstance(shots_per_weapon, int):
        shots = number_of_weapons * shots_per_weapon
    elif isinstance(shots_per_weapon, str):
        shots = 0
        for x in range(number_of_weapons):
            shots += roll_variable_dice(shots_per_weapon, target_unit_size, blast)

    if type == "Rapid Fire" and half_range:
        shots = shots*2

    return shots 

def calculate_damage(
    weapon: dict
):
    damage = weapon["D"]
    if isinstance(damage, str):
        damage = roll_variable_dice(damage)
    return damage

def roll_saves(
    defender: dict,
    weapon: dict,
    rolls: list[int]
):
    AP = weapon["AP"]
    save = defender["Sv"]
    inv = defender.get("inv", None)
    
    save_needed = max(save - AP, 2)

    if inv:
        save_needed = min(save_needed, inv)

    save_rolls = [roll_d6() for x in rolls]

    return [x for x in save_rolls if x < save_needed]


def shoot_weapon(
    attacker_bs: int,
    weapon: dict,
    defender: dict,
    half_range: bool = False,
    Leontus: bool = False,
    Leontus_balls: bool = False,
    regimental_standard: bool = False,
    castellan: bool = False,
    overcharged_las: bool = False,
    born_soldiers_trigger: Optional[int] = None,
    Creed: bool = False
):
    S = weapon["S"]

    number_of_shots = determine_number_of_shots(weapon=weapon, target_unit_size=defender["Model count"], half_range=half_range)

    hits = get_hit_rolls(shots=number_of_shots, BS=attacker_bs, castellan=castellan,leontus=Leontus, leontus_ballsy_hit=Leontus_balls, born_soldiers_trigger=born_soldiers_trigger)

    wounds = get_wound_rolls(hits=hits, S=S, T=T, BS=attacker_bs, leontus_ballsy_wound=Leontus_balls, leontus=Leontus, regimental_standard=regimental_standard, overcharged_las=overcharged_las, born_soldiers_trigger=born_soldiers_trigger)

    saves = roll_saves(defender=defender, weapon=weapon, rolls=wounds)

    damages_done = [calculate_damage(weapon) for x in saves]

    #TODO: Overcharged Las - add the mortal wounds bit here

    return damages_done


def make_shooting_attack(
    attacker: str,
    defender: str,
    born_soldiers_trigger: Optional[int], 
    half_range: bool = False, 
    FRFSRF: bool = False,
    Leontus: bool = False,
    Leontus_balls: bool = False,
    regimental_standard: bool = False,
    castellan: bool = False,
    overcharged_las: bool = False,
    Creed: bool = False
):
    unit_profiles = parse_unit_shooting_data()

    attacker_profile = unit_profiles.get(attacker, None)

    if not attacker_profile:
        raise NotImplementedError
    
    defender_profile = unit_profiles.get(defender, None)

    if not defender_profile:
        raise NotImplementedError

    attacker_bs = attacker_profile.get("BS", None)

    damage_done = []

    for weapon in attacker_profile["Weapons"]:
        weapon_profile = attacker_profile["Weapons"][weapon]
        if FRFSRF:
            if weapon in ["Hotshot Lasgun", "Lasgun"]:
                weapon_profile["Type"] = "Heavy"
                weapon_profile["Shots"] = 3
        damage_done += shoot_weapon(attacker_bs=attacker_bs, weapon=weapon_profile, defender=defender_profile, half_range=half_range, Leontus=Leontus, Leontus_balls=Leontus_balls, regimental_standard=regimental_standard, castellan=castellan, overcharged_las=overcharged_las, born_soldiers_trigger=born_soldiers_trigger, Creed=Creed)


def shock_troops_into_vanguard(
    BS: int = 4, 
    born_soldiers_trigger: int = 6, 
    half_range: bool = False, 
    FRFSRF: bool = False,
    Leontus: bool = False,
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

    if Leontus:
        las_attacks_leontus = [x for x in las_attacks if x >= BS] + [roll_d6() for x in las_attacks if x < BS]
        las_attacks = las_attacks_leontus

        plasma_attacks_leontus = [x for x in plasma_attacks if x >= BS] + [roll_d6() for x in plasma_attacks if x < BS]
        plasma_attacks = plasma_attacks_leontus

        autogun_attacks_leontus = [x for x in autogun_attacks if x >= BS] + [roll_d6() for x in autogun_attacks if x < BS]
        autogun_attacks = autogun_attacks_leontus

    elif castellan:
        las_attacks_castellan = [x for x in las_attacks if x > 1] + [roll_d6() for x in las_attacks if x == 1]
        las_attacks = las_attacks_castellan

        plasma_attacks_castellan = [x for x in plasma_attacks if x > 1] + [roll_d6() for x in plasma_attacks if x == 1]
        plasma_attacks = plasma_attacks_castellan

        autogun_attacks_castellan = [x for x in autogun_attacks if x > 1] + [roll_d6() for x in autogun_attacks if x == 1]
        autogun_attacks = autogun_attacks_castellan


    las_wounds = [roll_d6() for x in las_attacks if x >= BS] + [6 for x in las_attacks if x >= born_soldiers_trigger]
    plas_wounds = [roll_d6() for x in plasma_attacks if x >= BS and x < born_soldiers_trigger] + [6 for x in plasma_attacks if x >= born_soldiers_trigger]
    autogun_wounds = [roll_d6() for x in autogun_attacks if x >= BS and x < born_soldiers_trigger] + [6 for x in autogun_attacks if x >= born_soldiers_trigger]

    if Leontus:
        las_wounds_leontus = [roll_d6() for x in las_wounds if x < 4] + [x for x in las_wounds if x >= 4]
        las_wounds = las_wounds_leontus

        plas_wounds_leontus = [roll_d6() for x in plas_wounds if x < 2] + [x for x in plas_wounds if x >= 2]
        plas_wounds = plas_wounds_leontus

        autogun_wounds_leontus = [roll_d6() for x in autogun_wounds if x < 3] + [x for x in autogun_wounds if x >= 3]
        autogun_wounds = autogun_wounds_leontus
    
    elif regimental_standard:
        las_wounds_leontus = [roll_d6() for x in las_wounds if x == 1] + [x for x in las_wounds if x >= 1]
        las_wounds = las_wounds_leontus

        plas_wounds_leontus = [roll_d6() for x in plas_wounds if x == 1] + [x for x in plas_wounds if x >= 1]
        plas_wounds = plas_wounds_leontus

        autogun_wounds_leontus = [roll_d6() for x in autogun_wounds if x == 1] + [x for x in autogun_wounds if x >= 1]
        autogun_wounds = autogun_wounds_leontus

    las_saves = [roll_d6() for x in las_wounds if x >= 4]
    plas_saves = [roll_d6() for x in plas_wounds if x >= 2]
    autogun_saves = [roll_d6() for x in autogun_wounds if x >= 4]

    wounds = len([x for x in las_saves if x < 4] + [x for x in plas_saves if x < 5] + [x for x in autogun_saves if x < 4])

    return wounds

def tempestus_into_vanguard(
    BS: int = 3,
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

    if Leontus:
        las_attacks_leontus = [x for x in las_attacks if x >= BS] + [roll_d6() for x in las_attacks if x < BS]
        las_attacks = las_attacks_leontus

        plasma_attacks_leontus = [x for x in plasma_attacks if x >= BS] + [roll_d6() for x in plasma_attacks if x < BS]
        plasma_attacks = plasma_attacks_leontus

        las_volley_attacks_leontus = [x for x in las_volley_attacks if x >= BS] + [roll_d6() for x in las_volley_attacks if x < BS]
        las_volley_attacks = las_volley_attacks_leontus

    elif castellan:
        las_attacks_castellan = [x for x in las_attacks if x > 1] + [roll_d6() for x in las_attacks if x == 1]
        las_attacks = las_attacks_castellan

        plasma_attacks_castellan = [x for x in plasma_attacks if x > 1] + [roll_d6() for x in plasma_attacks if x == 1]
        plasma_attacks = plasma_attacks_castellan

        las_volley_attacks_castellan = [x for x in las_volley_attacks if x > 1] + [roll_d6() for x in las_volley_attacks if x == 1]
        las_volley_attacks = las_volley_attacks_castellan

    las_wounds = [roll_d6() for x in las_attacks if x >= BS] + [roll_d6() for x in las_attacks if x == 6]
    plas_wounds = [roll_d6() for x in plasma_attacks if x >= BS] + [roll_d6() for x in plasma_attacks if x == 6]
    las_volley_wounds = [roll_d6() for x in las_volley_attacks if x >= BS] + [roll_d6() for x in las_volley_attacks if x == 6]

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
    las_volley_saves = [roll_d6() for x in las_volley_wounds if x >= 3]

    wounds = len([x for x in las_saves if x < 5] + [x for x in plas_saves if x < 5] + [x for x in las_volley_saves if x < 5])
    
    if overcharged_las:
        wounds += min(6, number_of_sixes)

    return wounds

def kasrkin_into_vanguard(
    BS: int = 3, 
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
        las_attacks_leontus = [x for x in las_attacks if x >= BS] + [roll_d6() for x in las_attacks if x < BS]
        las_attacks = las_attacks_leontus

        plasma_attacks_leontus = [x for x in plasma_attacks if x >= BS] + [roll_d6() for x in plasma_attacks if x < BS]
        plasma_attacks = plasma_attacks_leontus

        las_volley_attacks_leontus = [x for x in las_volley_attacks if x >= BS] + [roll_d6() for x in las_volley_attacks if x < BS]
        las_volley_attacks = las_volley_attacks_leontus

    elif castellan:
        las_attacks_castellan = [x for x in las_attacks if x > 1] + [roll_d6() for x in las_attacks if x == 1]
        las_attacks = las_attacks_castellan

    las_wounds = [roll_d6() for x in las_attacks if x >= BS] + [6 for x in las_attacks if x >= born_soldiers_trigger]
    plas_wounds = [roll_d6() for x in plasma_attacks if x >= BS and x < born_soldiers_trigger] + [6 for x in plasma_attacks if x >= born_soldiers_trigger]
    las_volley_wounds = [roll_d6() for x in las_volley_attacks if x >= BS and x < born_soldiers_trigger] + [6 for x in las_volley_attacks if x >= born_soldiers_trigger]

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
