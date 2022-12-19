from statistics import mean

from combat import attack

def run_simulation(iterations: int, profile: dict):

    wounds = [attack(**profile)[1] for x in range(iterations)]

    return mean(wounds)
