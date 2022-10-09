import json
from enum import Enum
import datetime
import time

class Location(Enum):
    HOME = 0
    SHOPS = 1
    UNI = 2
    GYM = 3
    WORK = 4

    def __str__(self) -> str:
        return super().__str__().replace("Location.", "")
    
    @staticmethod
    def fromString(string: str) -> 'Location':
        dic = {str(loc): loc for loc in Location}
        
        try:
            return dic[string]
        except KeyError:
            return Location.HOME
    
    @staticmethod
    def asList() -> 'list[Location]':
        return [Location.HOME, Location.SHOPS, Location.UNI, Location.GYM, Location.WORK] 



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
        return "<ID: " + self.id + " NAME: " + self.name + " LOCATION: " + str(self.location) + ">"

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
    def decode(self, s: 'str') -> 'Resident':
        obj = json.loads(s)

        fields = {"id", "name", "location"}

        if any(field not in obj.keys() for field in fields):
            raise json.JSONDecodeError("Not an appropriate Resident object for this decoder", s) 

        resident = Resident(obj["id"], obj["name"])
        resident.location = Location.fromString(obj["location"])
        return resident

class Appliance:
    '''
    Generic Appliance class
    '''
    mode: 'str'
    timestamp: 'datetime.datetime'
    name: 'str'

    def __init__(self, name):
        self.name = name
        self.mode = self.setMode("AVAILABLE")
        self.timestamp = datetime.datetime.now()

    def setMode(self, mode: 'str') -> str:
        if mode not in ["DONE", "INUSE", "AVAILABLE"]:
            return self.mode
        else:
            self.mode = mode

        return self.mode
