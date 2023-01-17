import json

from os import listdir

def parse_unit_shooting_data():
    output = {}
    
    for file in listdir('shooting_unit_profiles'):
        with open('shooting_unit_profiles/' + file, 'r') as fb:
            output = {**output, **json.loads(fb.read())}
    
    return output
