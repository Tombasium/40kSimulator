from simulate import run_simulation

from attackProfiles import attack_profiles

from utils import generate_result_string

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
