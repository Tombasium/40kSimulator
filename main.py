from combat import attack

from utils import *

from simulate import run_simulation

from unit import Unit

from control import run

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

a = {
    'a': 1,
    'b': 2
}

for i in a.items():
    print(i[0])
