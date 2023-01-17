from typing import Optional

from utils import make_word_green, make_word_red, roll_d6

def determine_wound_roll_needed(
    S: int, 
    T :int,
    WRAmod: int = 0,
    WRDmod: int = 0
):
    if S >= 2*T:
        needed_roll_to_wound = 2
    elif S > T:
        needed_roll_to_wound = 3
    elif S == T:
        needed_roll_to_wound = 4
    elif S <= T/2:
        needed_roll_to_wound = 6
    else:
        needed_roll_to_wound = 5

    return needed_roll_to_wound - WRAmod + WRDmod

def roll_to_hit(
    debug: bool, 
    WS: int, 
    HRAmod: int,
    HRDmod: int
    ):

    roll_needed = WS + HRDmod - HRAmod

    hit_roll = roll_d6()
    if hit_roll == 1:
        if debug: 
            print('Attack {0} with roll of {1}'.format(make_word_red('misses'), hit_roll))
        return 
    if (hit_roll == 6 or hit_roll >= roll_needed) and hit_roll != 1:
        if debug: 
            print('Attack {0} with roll of {1}'.format(make_word_green('hits'), hit_roll))
        return hit_roll
    else:
        if debug: 
            print('Attack {0} with roll of {1}'.format(make_word_red('misses'), hit_roll))
        return 

def roll_to_wound(
    debug: bool, 
    S: int, 
    T: int,
    WRAmod: int,
    WRDmod: int
    ):
    
    if S >= 2*T:
        needed_roll_to_wound = 2
    elif S > T:
        needed_roll_to_wound = 3
    elif S == T:
        needed_roll_to_wound = 4
    elif S <= T/2:
        needed_roll_to_wound = 6
    else:
        needed_roll_to_wound = 5
    
    needed_roll_to_wound = needed_roll_to_wound + WRDmod - WRAmod

    wound_rolled = roll_d6()

    if wound_rolled >= needed_roll_to_wound:
        if debug: 
            print('Attack {0} with roll of {1}'.format(make_word_green('wounds'), wound_rolled))
        return wound_rolled
    else:
        if debug: 
            print('Attack {0} with roll of {1}'.format(make_word_red('fails'), wound_rolled))
        return

def roll_to_save(
    debug: bool, 
    Sv: int, 
    inv: Optional[int], 
    AP: int
    ):
    
    save_needed = min(Sv + AP, inv) if inv else Sv + AP 
    
    save_result = roll_d6()

    if save_result >= save_needed:
        if debug: 
            print('Wound {0} with roll of {1}'.format(make_word_red('saved'), save_result))
        return 
    else: 
        if debug: 
            print('Wound {0} with roll of {1}'.format(make_word_green('gets through'), save_result))
        return save_result

def attack(
    A: int, 
    S: int, 
    WS: int, 
    T: int, 
    Sv: int, 
    Dam: int = 1,
    AP: int = 0, 
    HRAmod: int = 0, 
    HRDmod: int = 0, 
    WRAmod: int = 0,
    WRDmod: int = 0,
    inv: Optional[int] = None,
    xplode: Optional[int] = None,
    debug: bool = False
    ):
    
    if debug: 
        print(f'Rolling {A} attacks:\n')

    hits = [roll_to_hit(debug, WS, HRAmod, HRDmod) for x in range(A)]

    if xplode:
        exploding_hits = len([hit for hit in hits if hit is not None and hit >= xplode])
        if debug: 
            print('')
            print(f'Got {exploding_hits} sixes to hit!')
            print('')
        hits += [roll_to_hit(debug, WS, HRAmod, HRDmod) for x in range(exploding_hits)]
    
    if debug: 
        print('')

    wounds = [roll_to_wound(debug, S, T, WRAmod, WRDmod) for x in hits if x is not None]

    if debug: 
        print('')

    not_saved = [roll_to_save(debug, Sv, inv, AP) for x in wounds if x is not None]

    if debug: 
        print('')

    hits_count = len([result for result in not_saved if result is not None])

    dmg_ttl = hits_count * Dam

    if debug:
        print(f'\n{hits_count} get through from {A} Attacks causing {dmg_ttl} wounds')

    return (hits_count, dmg_ttl)
