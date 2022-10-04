import librosa
import os
import json
import soundfile as sf

from typing import Optional
from pydantic import BaseModel

DATA_FILE_PATH = 'mp_ev_v3.json'
DATA_AUDIO_FILES = '/home/vpoblete/Escritorio'
class Event(BaseModel):
    taxonomy: str
    start: float|int
    end: float|int
    length: float|int
    file_name: str

def importData():
    with open(DATA_FILE_PATH) as file:
        data = json.load(file)
        return data
        events = [Event(**event) for event in data]
    return events

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
    y = x[start*sr : end*sr]
    return y, sr

def writeAudioFile(data, sr, file_name: str, taxonomy:str):
    base_path = 'taggin\media'
    directory = os.path.join(base_path, taxonomy)
    path = os.path.join(directory, file_name)
    sf.write(path, data, sr)

def loopThroughTheData(directory: Optional[str]=None) -> None:
    events = importData()
    
    for i, event in enumerate(events):
        if directory:
            path = os.path.join(directory, event.file_name)
        y, sr = cutAudioFile(path, 
                            event.start,
                            event.end)
        writeAudioFile(y, sr, f'{event.file_name}_{i+1}', event.taxonomy)

def main() -> None:
    """Main function"""
    #loopThroughTheData(DATA_FILE_PATH)
    events = importData()

if __name__ == '__main__':
    main()