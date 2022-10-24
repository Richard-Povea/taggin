from dataclasses import dataclass
from typing import Tuple
import numpy as np

#Constants
N = 10
RESOLUTION = 1
ROOM_SIZE = 250
CENTER = round(ROOM_SIZE/2)

HUMEDAL = (2, 100)
HUMEDAL_URBANO = (100, 200)
URBANO = (200, 249)

@dataclass
class Environments():
    prob_h: int
    prob_h_u: int
    prob_u: int
    
    def __post_init__(self):
        self.restriction = HUMEDAL
        self.humedal = self.__get_range()
        self.restriction = HUMEDAL_URBANO
        self.humedal_urbano = self.__get_range()
        self.restriction = URBANO
        self.urbano = self.__get_range()
    
    def __get_range(self):
        return self.__position_range()
    
    def __position_range(self):
        if isinstance(self.restriction, (int, float)):
            return self.restriction
            
        array = np.round(np.arange(-round(self.restriction[1]/2), 
                          round(self.restriction[1]/2)+RESOLUTION, 
                          RESOLUTION),1)
        return self.__del_range(array)
    
    def __del_range(self, array):
        low = self.restriction[0]
        if low == 2:
            mask = np.where((array <= -low) | (array >= low))
            return array[mask] + CENTER
        mask = np.where((array <= -self.restriction[0]/2) | (array >= self.restriction[0]/2))
        return array[mask] + CENTER
        
    