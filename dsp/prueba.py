import librosa
import os
import json
from typing import Optional
import soundfile as sf

DATA_AUDIO_FILES = '/home/vpoblete/Escritorio/audio_signals'
DATA_FILE_PATH = '/home/vpoblete/Escritorio/richard/taggin/mp_ev_v3.json'


def importData():
    with open(DATA_FILE_PATH) as file:
        data = json.load(file)
        return data

def loopThroughTheData(directory: Optional[str]=None) -> None:
    events = importData()
    
    for i, event in enumerate(events):
        if directory:
            path = os.path.join(directory, event['file_name'])
        y, sr = cutAudioFile(path, 
                            event['start'],
                            event['end'])
        writeAudioFile(y, sr, '{}_{}'.format(i+1, event['file_name']), event['taxonomy'])

def cutAudioFile(path: str, start: float|int, end: float|int):
    """Cut an audio file\n
        PARAMETERS:
            path: relative path\n
            start: start of output audio\n
            end: end of output audio\n
            name: name of output file
            output_path: output file directory
    """
    x, sr = librosa.load(path, sr=None)
    y = x[int(start*sr) : int(end*sr)]
    return y, sr

def writeAudioFile(data, sr: int, file_name: str, taxonomy:str):
    base_path = '/home/vpoblete/Escritorio/richard/taggin/media'
    directory = os.path.join(base_path, taxonomy)
    path = os.path.join(directory, file_name)
    sf.write(path, data, sr)

def main() -> None:
    """Main function"""
    #loopThroughTheData(DATA_FILE_PATH)
    events = loopThroughTheData(DATA_AUDIO_FILES)

if __name__ == '__main__':
    main()