from random import randint

def roll_d6():
    return randint(1, 6)

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
