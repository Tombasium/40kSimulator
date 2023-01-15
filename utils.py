from random import randint
from os import listdir
import json

def roll_d6():
    return randint(1, 6)

def roll_d3():
    return randint(1, 3)

def roll_2d6():
    return randint(1, 6) + randint(1, 6)

def make_word_red(word: str) -> str:
    return f'\033[0;31m{word}\033[0;37m'

def make_word_green(word: str) -> str:
    return f'\033[0;32m{word}\033[0;37m'

def make_word_yellow(word: str) -> str:
    return f'\033[1;33m{word}\033[0;37m'

def make_word_cyan(word: str) -> str:
    return f'\033[0;36m{word}\033[0;37m'

def make_word_purple(word: str) -> str:
    return f'\033[0;35m{word}\033[0;37m'

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

def parse_unit_data():
    output = {}
    
    for file in listdir('units'):
        with open('units/' + file, 'r') as fb:
            output = {**output, **json.loads(fb.read())}
    
    return output

def parse_model_data():
    output = {}
    
    for file in listdir('models'):
        with open('models/' + file, 'r') as fb:
            output = {**output, **json.loads(fb.read())}
    
    return output

def parse_weapon_data():
    output = {}
    
    for file in listdir('weapons'):
        with open('weapons/' + file, 'r') as fb:
            output = {**output, **json.loads(fb.read())}
    
    return output
