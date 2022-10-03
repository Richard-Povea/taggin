import librosa
import os
import json
import soundfile as sf

from typing import Optional
from pydantic import BaseModel, validator, ValidationError

DATA_FILE_PATH = 'mp_ev_v3.json'

class Event(BaseModel):
    taxonomy: str
    start: float|int
    end: float|int
    length: float|int
    file_name: str

def importData() -> Event:
    with open(DATA_FILE_PATH) as file:
        data = json.load(file)
        events = [Event(**e) for e in data]
    return events

def cutAudioFile(path: str, start: float|int, end: float|int, name: str, output_path: Optional[str]=None) -> None:
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
    if output_path:
        name = os.path.join(output_path, name)
    sf.write(name, y, sr)

def loopThroughTheData(directory: Optional[str]=None) -> None:
    events = importData()
    if directory:
        path = os.path.join(directory, event.file_name)
    for i, event in enumerate(events):
        cutAudioFile(path, 
                     event.start,
                     event.end,
                     f'{event.file_name}_{i+1}')

def main() -> None:
    """Main function"""
    loopThroughTheData()

if __name__ == '__main__':
    main()