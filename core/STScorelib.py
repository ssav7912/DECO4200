import json
from enum import Enum


class Location(Enum):
    HOME = 0
    SHOPS = 1
    UNI = 2
    GYM = 3
    WORK = 4

    def __str__(self) -> str:
        return super().__str__().replace("Location.", "")

class Resident:
    '''
    Resident class. Stores the user id, name and current location of the resident.
    '''
    id: str
    name: str
    location: 'Location' 

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.location = Location.HOME

    def __repr__(self) -> 'str':
        return "<ID:" + self.id + "NAME:" + self.name + ">"

    def move_location(self, location: 'Location') -> bool:
        if location is self.location:
            return False
        else:
            self.location = location
            #invoke movement?
            return True

    def toJson(self):
        dic = {"id": self.id, "name": self.name, "location": self.location}

        return json.dumps(dic)

class ResidentDecoder(json.JSONDecoder):
    def decode(s: 'str') -> 'Resident':
        obj = json.loads(s)

        fields = {"id", "name"}

        if any(field not in obj.keys() for field in fields):
            raise json.JSONDecodeError("Not an appropriate Resident object for this decoder", s) 

        return Resident(obj["id"], obj["name"])
