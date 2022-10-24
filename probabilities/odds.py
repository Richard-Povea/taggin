from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Sequence, Tuple
from config_environments import Environments

from tqdm import tqdm

import yaml
import numpy as np
import pandas as pd
import timeit


#Constants
N = 20
DELTA = 2
RESOLUTION = 1
ROOM_SIZE = 250
CENTER = round(ROOM_SIZE/2)
HUMEDAL = (2, 99)
HUMEDAL_URBANO = (100, 199)
URBANO = (200, 249)

def main():
    taxonomies = create_taxonomies()
    positions = RandomPositions(52)
    loop = tqdm(total = N, position=0, leave=False)
    for i in range(1,N+1):
        #loop.set_description('Loading ...')
        loop.update(1)
        auxiliary = dict()
        for  taxonomy in taxonomies:
            item: Taxonomy = taxonomies[taxonomy]
            event = item.get_event()
            auxiliary[item.name] = positions.random_position(event, item.high_limits)
        if i == 1:
            series = pd.Series(auxiliary, name=i)
            continue
        series = pd.concat([series, pd.Series(auxiliary, name=i)], axis=1)
    loop.close()
    series = pd.DataFrame(series.T)
    series.to_csv('test20.csv')
    
def create_taxonomies():
    taxonomies = dict()
    for index, data in enumerate(TaxonomyNames):
        taxonomy = Taxonomy(data, RandomOdds(42+index))
        taxonomies[taxonomy.name] : Taxonomy = taxonomy
    return taxonomies

def iterate_config(config:dict) -> list[dict]:
    return [iterate_scenario(config[setting]) for setting in config]
    
def iterate_scenario(setting:dict) -> dict:
    odds = dict()
    for taxonomy, value in setting.items():
        lam = value[0]
        max = value[1]
        odds[taxonomy] = [get_odd(lam, max) for _ in range(N)]
    return odds
    
def import_config(filename:str) -> dict:
    with open(filename) as file:
        odds = yaml.load(file, Loader=yaml.FullLoader)
    return odds

def get_odd_integers(rng, min, max, total) -> int:
    amount = rng.integers(min, max)
    while np.sum(amount) > total:
        amount = rng.integers(min, max)
    return amount

def create_scenario(setting: dict, name: str):
    positions = dict()
    restrictions = import_config(r'probabilities\taxonomy_restrictions.yaml')
    for taxonomy in setting:
        tax_restrictions = restrictions[taxonomy]
        a = TaxonomyRange(tax_restrictions['x'], 
                     tax_restrictions['y'], 
                     tax_restrictions['z'])
        positions[taxonomy] = list(map(lambda pos: [a.random_position() for _ in range(pos)] ,setting[taxonomy]))
        del a
    return positions

def calculate_range(range: Tuple[int, int]):
    setting = np.arange(-range[1]//2,range[1]//2 + RESOLUTION, RESOLUTION)
    mask = np.where((-range[0]//2 > setting) | (setting > range[0]//2))
    return setting[mask]+CENTER

class TaxonomyNames(Enum):
    FROG = 'frog'
    BIRD = 'bird'
    DOG = 'dog'
    CAR = 'car'
    STEP = 'step'
    MURMULLO = 'murmullo'

@dataclass
class RandomOdds:
    rng_seed: int | float
    
    
    def __post_init__(self):
        self.rng =  np.random.default_rng(seed=self.rng_seed)
        
    def n_events(self, odds: Tuple[int|float, int|float, int|float]):
        return self.rng.poisson(odds).astype('int8')
    
@dataclass
class Settings:
    config_path = 'probabilities\config.yaml'
    name: TaxonomyNames
    
    def __post_init__(self):
        self.config = import_config(self.config_path)
        self.name = self.name.value
    
    @property
    def environment(self) -> Tuple[int, int, int]:
        return self.config['environment'][self.name]
    
    @property
    def n_limits(self):
        limits = self.config['min_max'][self.name]
        return tuple([limit[0] for limit in limits]), tuple([limit[1] for limit in limits])
    
    @property
    def high_limits(self) -> float|Tuple[float, float]:
        limit = self.config['high_limit'][self.name]
        if isinstance(limit, Tuple):
            return np.arange(limit[0], limit[1])
        return limit

class RandomPositions:
    HUMEDAL = (2, 99)
    HUMEDAL_URBANO = (100, 199)
    URBANO = (200, 249)
    
    def __init__(self, seed:int) -> None:
        self.seed = seed
        self.rng = np.random.default_rng(seed=self.seed)
        self.range_H = calculate_range(HUMEDAL)
        self.range_HU = calculate_range(HUMEDAL_URBANO)
        self.range_U = calculate_range(URBANO)
        
    
    def random_position(self, n_events: Tuple[int, int, int], high: float) -> Sequence:
        positions = []
        if not isinstance(high, float):
            high = self.rng.choice(high)
        humedal_events, humedal_urbano_events, urbano_events = n_events
        if humedal_events:
            for _ in range(humedal_events):
                positions.append((self.rng.choice(self.range_H), 
                                high, 
                                -self.rng.choice(self.range_H)))
                
        if humedal_urbano_events:
            for _ in range(humedal_urbano_events):
                positions.append((self.rng.choice(self.range_HU), 
                                  high, 
                                  -self.rng.choice(self.range_HU)))
        if urbano_events:
            for _ in range(urbano_events):
                positions.append((self.rng.choice(self.range_U), 
                                  high, 
                                  -self.rng.choice(self.range_U)))
        return np.array(positions, dtype=object)

class Taxonomy:
    n_events: int = 0
    
    def __init__(self, name: TaxonomyNames, rng: RandomOdds) -> None:
        self.name: str = name.value
        self.rng = rng
        self.settings = Settings(name)
    
    def __repr__(self):
        return (f'''{self.name.capitalize()} with {self.settings.environment} odds\n
                {self.high_limits} high limits and\n
                {self.settings.n_limits} as minimum and maximum number of {self.name}s respectively.\n''')
    
    def get_event(self):
        lower, upper = self.settings.n_limits
        odds = self.settings.environment
        event = self.rng.n_events(odds)
        while any(event < lower) or any(event > upper):
            event = self.rng.n_events(odds)
        return event
    
    @property
    def high_limits(self):
        return self.settings.high_limits
                
@dataclass
class TaxonomyRange():
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
    # TEST_CODE = 'import numpy as np'
    # print(np.median(timeit.repeat(setup=TEST_CODE,stmt=main, repeat=50, number=1)))
    main()