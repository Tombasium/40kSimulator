from combat import attack

from utils import *

from simulate import run_simulation

from attackProfiles import attack_profiles

def generate_result_string(
    attacker: str, 
    defender: str, 
    waagh: bool,
    wounds: float
) -> str:
    attacker = make_word_cyan(attacker)
    defender = make_word_purple(defender)
    waaghstring = ''
    if waagh:
        waaghstring = make_word_yellow('on a waagh!!! ')
    wounds = make_word_green(str(wounds))
    return f'{attacker} hits {defender} {waaghstring}for {wounds}\n'


for profile in attack_profiles:
    if profile['defender'] == 'Tyranid Warriors':
        attacker = profile['attacker']
        defender = profile['defender']
        result = run_simulation(10000, profile['profile'])
        print(generate_result_string(
            profile['attacker'],
            profile['defender'],
            profile['waagh'],
            result
        ))



# nobs_no_waagh = run_simulation(
#     iterations=10000,
#     profile=nob_no_waagh_profile
# )

# nobs_waagh = run_simulation(
#     10000, 
#     nob_waagh_profile
# )

# snaggas_no_waagh = run_simulation(
#     10000, 
#     snaggas_no_waagh_profile
# )

# snaggas_waagh = run_simulation(
#     10000, 
#     snaggas_waagh_profile
# )

# boyz_no_waagh = run_simulation(
#     10000, 
#     boyz_no_waagh_profile
# )

# boyz_waagh = run_simulation(
#     10000, 
#     boyz_waagh_profile
# )

# # print('vs {0}...'.format(make_word_red('Daemons')))

# # print('\nNobs normally do {0} wounds'.format(make_word_green(str(nobs_no_waagh))))
# # print('Nobs on Waagh do {0} wounds'.format(make_word_green(str(nobs_waagh))))

# # print('\nBeast Snaggas normally do {0} wounds'.format(make_word_green(str(snaggas_no_waagh))))
# # print('Beast Snaggas on Waagh do {0} wounds'.format(make_word_green(str(snaggas_waagh))))

# # print('\nBoyz normally do {0} wounds'.format(make_word_green(str(boyz_no_waagh))))
# # print('Boyz on Waagh do {0} wounds'.format(make_word_green(str(boyz_waagh))))

# print('vs {0}...'.format(make_word_red('Tyranids')))

# print('\nNobs normally do {0} wounds'.format(make_word_green(str(nobs_no_waagh))))
# print('Nobs on Waagh do {0} wounds'.format(make_word_green(str(nobs_waagh))))

# print('\nBeast Snaggas normally do {0} wounds'.format(make_word_green(str(snaggas_no_waagh))))
# print('Beast Snaggas on Waagh do {0} wounds'.format(make_word_green(str(snaggas_waagh))))

# print('\nBoyz normally do {0} wounds'.format(make_word_green(str(boyz_no_waagh))))
# print('Boyz on Waagh do {0} wounds'.format(make_word_green(str(boyz_waagh))))
