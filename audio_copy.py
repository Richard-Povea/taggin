import pandas as pd
import numpy as np
import os
import shutil

BASE_PATH = ''
OUTPUT_PATH = ''

data = pd.read_csv('data_resumen.csv', 
                   index_col=0)

for audio in data.index:
    shutil.copy(os.path.join(BASE_PATH, audio), os.path.join(OUTPUT_PATH, audio))
