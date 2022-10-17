from dataclasses import dataclass, replace
import librosa
import os
import soundfile as sf
import numpy as np
import re
import shutil 

FROGS_PATH = 'D:/mediaData/frogs'

BASE_PATH = 'D:/Cosas U/TESIS/Distancia - FUSA/Audios/Audios Richard/vehículos'
DESTINY_PATH = 'D:/mediaData/vehicle'

EDITS_PATH = 'D:/GITHUB/taggin/media/edits'
SELECTED_PATH = 'D:/mediaData/selected'

AMPHIBIANS = {'Batrachyla_leptopus', 
              'Batrachyla_taeniata', 
              'Pleurodema_thaul', 
              'other_amphibians'}
name = 'frog001'

def changeAmphibiansName(path: str):
    for amphibian in AMPHIBIANS:
        output_path = os.path.join(path, amphibian)  
        searchFiles(output_path)

def copy_files(base_path: str, destiny_path: str, file_name: str) -> None:
    file_name += '001'
    with os.scandir(base_path) as files:
        for file in files:
            shutil.copyfile(file.path, os.path.join(destiny_path, file_name)+'.wav')
            file_name = updateName(file_name)
                
def searchFiles(dir: str):
    global name
    with os.scandir(dir) as files:
        data = configFile('', name, FROGS_PATH)
        for file in files: 
            data.path = file.path
            data.load_file()
            data.normalizeFile()
            data.writeFile()
            data.name = updateName(data.name)
            break
        name = data.name

def updateName(name: str):
    res = re.sub(r'[0-9]+$', 
            lambda x: f"{str(int(x.group())+1).zfill(len(x.group()))}",  
            name)
    return res

@dataclass
class configFile:
    path: str
    name: str
    output_path: str
    
    def load_file(self) -> None:
        self.x, self.sr = librosa.load(self.path, sr=None)
    
    def normalizeFile(self) -> None:
        self.x = self.x/np.linalg.norm(self.x, np.inf)

    def writeFile(self):
        output_path = os.path.join(self.output_path, self.name+'.wav')
        sf.write(output_path, self.x, self.sr)
    
    

    
def main()->None:
    # changeAmphibiansName(SELECTED_PATH)
    # changeAmphibiansName(EDITS_PATH)
    copy_files(BASE_PATH, DESTINY_PATH, 'vehicle')
    
if __name__ == '__main__':
    main()
