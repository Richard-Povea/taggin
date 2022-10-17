from dataclasses import dataclass
from typing import Tuple

import yaml
import numpy as np
import pandas as pd
import timeit

#Constants
OPTIONS = np.arange(0, 3)
# TAXONOMY_RESTRICTIONS = import_config()
N = 10
DELTA = 2
RESOLUTION = 1
ROOM_SIZE = 250
CENTER = round(ROOM_SIZE/2)


def main():
    config = import_config('probabilities\config.yaml')
    humedal, humedal_urbano, urbano = iterate_config(config)
    setting = create_scenario(humedal, 'humedal')
    export(setting)
    
def iterate_config(config:dict) -> list[dict]:
    return [iterate_scenario(config[setting]) for setting in config]
    
def iterate_scenario(setting:dict) -> dict:
    odds = dict()
    for taxonomy, value in setting.items():
        odds[taxonomy] = [get_odd(value) for _ in range(N)]
    return odds
    
def import_config(filename: str) -> dict:
    with open(filename) as file:
        odds = yaml.load(file, Loader=yaml.FullLoader)
    return odds

def get_odd(mu:int) -> int:
    data = np.random.poisson(mu)
    if not ( data <=3):
        while not (data <=3):
            data = np.random.poisson(mu)
    return data

def create_scenario(setting: dict, name: str):
    positions = dict()
    restrictions = import_config(r'probabilities\taxonomy_restrictions.yaml')
    for taxonomy in setting:
        tax_restrictions = restrictions[taxonomy]
        a = Taxonomy(tax_restrictions['x'], 
                     tax_restrictions['y'], 
                     tax_restrictions['z'])
        positions[taxonomy] = list(map(lambda pos: [a.random_position() for _ in range(pos)] ,setting[taxonomy]))
        del a
    return positions

@dataclass
class Taxonomy():
    x_restriction: tuple
    y_restriction: Tuple | int | float
    z_restriction: tuple
    
    def __post_init__(self):
        self.x_range = self.__position_range(self.x_restriction)
        self.y_range = (np.arange(self.y_restriction[0], self.y_restriction[1]) 
                        if isinstance(self.y_restriction, tuple) 
                        else self.y_restriction)
        self.z_range = self.__position_range(self.z_restriction)
    
    def __position_range(self, restriction: Tuple | int | float):
        if isinstance(restriction, (int, float)):
            return restriction
        
        array = np.round(np.arange(-(restriction[1]/2-DELTA), 
                          restriction[1]/2-DELTA+RESOLUTION, 
                          RESOLUTION),1)
        return self.__del_range(array, restriction[0])
    
    def __del_range(self, array, restriction: int):
        mask = np.where((array <= -restriction/2) | (array >= restriction/2))
        return array[mask]
        
    def random_position(self):
        y = self.y_range
        x = np.random.choice(self.x_range) + CENTER
        y = np.random.choice(y) if not isinstance(y, (int, float)) else y
        z = -(np.random.choice(self.z_range) + CENTER)
        return (x, y, z)
    
def export(data: dict):
    output = pd.DataFrame(data)
    output.to_csv('data.csv')
    
if __name__ == '__main__':
    TEST_CODE = 'import numpy as np'
    #print(timeit.timeit(setup=TEST_CODE,stmt=main, number=4))
    main()