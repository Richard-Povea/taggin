import librosa
import os
import pydantic
import soundfile as sf
from typing import Optional

DATA_FILE_PATH = r'C:\Users\richa\OneDrive - Universidad Austral de Chile\PSELD\taggin file\monophonic_events.json'

FILE = './Hola a todos lo gamers.wav'
START = 0
END = 1

class Event(pydantic.BaseModel):
    taxonomy: str
    beginning: float|int
    end: float|int
    length: float|int

def cutAudioFile(path: str, start: float|int, end: float|int, name: str, output_path: Optional[str]=None) -> None:
    """Cut an audio file\n
        PARAMETERS:
            path: directory or file name\n
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



def main() -> None:
    """Main function"""
    cutAudioFile(FILE, START, END, 'test.wav')

if __name__ == '__main__':
    main()