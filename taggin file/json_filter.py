import json
import pydantic
import json

from typing import List

class Event(pydantic.BaseModel):
    path: str
    beginning: float
    end: float
    taxonomy: str


def main() -> None:
    """"Main function"""
    #Read data from a JSON file
    with open("./1039_modificado_v2.json") as file:
        data = json.load(file)
        events: List[Event] = [Event(**item) for item in data]
        print(events[0].taxonomy)
        
if __name__ == "__main__":
    main()
