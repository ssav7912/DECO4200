import json
from enum import Enum
import datetime
import time
import numpy as np

ELECUSAGEMONTH: 'np.ndarray' = np.interp([np.random.random() for x in range(30)], [0, 1], [20, 25]) 
ELECUSAGEDAY: 'np.ndarray' = np.interp([np.random.random() for x in range(24)], [0, 1], [0, 1])

WATERUSAGEMONTH: 'np.ndarray' = np.interp([np.random.random() for x in range(30)], [0, 1], [180*3, 220*3])
WATERUSAGEDAY: 'np.ndarray' = np.interp([np.random.random() for x in range(24)], [0,1], [(180*3)/24, (220*3)/24])

GASUSAGEMONTH: 'np.ndarray' = np.interp([np.random.random() for x in range(30)], [0, 1], [20, 23])
GASUSAGEDAY: 'np.ndarray' = np.interp([np.random.random() for x in range(24)], [0, 1], [20/24, 23/24])

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

class Status(Enum):
    AWAY = "Away"
    BUSY = "Busy"
    AVAILABLE = "Available"
    DONOTDISTURB = "Do not Disturb"

    def __str__(self) -> str:
        return super().value

    @staticmethod
    def fromString(string: str) -> 'Status':
        dic = {str(status) : status for status in Status}

        try:
            return dic[string]
        except KeyError:
            return Status.AVAILABLE

    @staticmethod
    def asList() -> 'list[Status]':
        return [status for status in Status]


class Utility(Enum):
    ELECTRICITY = 0
    WATER = 1
    GAS = 2

class Resident:
    '''
    Resident class. Stores the user id, name and current location of the resident.
    '''
    id: str
    name: str
    location: 'Location' 
    status: 'Status'

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.location = Location.HOME
        self.status = Status.AVAILABLE

    def __repr__(self) -> 'str':
        return "<ID: " + self.id + " NAME: " + self.name + " LOCATION: " + str(self.location) + "STATUS:" + str(self.status) + ">"

    def move_location(self, location: 'Location') -> bool:
        if location is self.location:
            return False
        else:
            self.location = location
            #invoke movement?
            return True

    def toJson(self):
        dic = {"id": self.id, "name": self.name, "location": self.location, "status": self.status}

        return json.dumps(dic)

class ResidentDecoder(json.JSONDecoder):
    def decode(self, s: 'str') -> 'Resident':
        obj = json.loads(s)

        fields = {"id", "name", "location", "status"}

        if any(field not in obj.keys() for field in fields):
            raise json.JSONDecodeError("Not an appropriate Resident object for this decoder", s) 

        resident = Resident(obj["id"], obj["name"])
        resident.location = Location.fromString(obj["location"])
        resident.status = Status.fromString(obj["status"])
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

class Home:
    name: str
    appliances: 'list[Appliance]'
    lights: 'list[bool]'
    residents: 'list[Resident]'
    utilities: 'set[Utility]'

    def __init__(self, name: str, numlights: int):
        self.name = name
        self.appliances =  []
        self.residents = []
        self.lights = [False for x in range(numlights)]
        self.utilities = {Utility.ELECTRICITY}
    

    def init_lights(self, numlights: int) -> None:
        self.lights = [False for x in range(numlights)]

    def togglelight(self, index: 'int', SetOn: bool) -> bool:

        oldvalue = self.lights[index]
        self.lights[index] = SetOn

        return oldvalue
        

    def getLightsOn(self) -> int:
        i = 0
        for light in self.lights:
            if light is True:
                i+= 1

        return i

        
    def addAppliance(self, appliance: 'Appliance') -> None:
        self.appliances.append(appliance)

    def getApplianceByName(self, name: 'str') -> 'Appliance':
        for appliance in self.appliances:
            if appliance.name == name:
                return appliance
        else:
            raise KeyError("No such appliance with that name")

    def querySmartMeter(self, pstart: 'datetime.datetime', pend: 'datetime.datetime') -> 'np.ndarray':
        '''
        Unimplemented! Returns Test Data

        Should query some smart meter API to retrieve electricity usage over the specified time period, returning it as an array.
        '''
        #what's the average daily usage?

        if abs((pstart - pend).days) <= 1:

            return ELECUSAGEDAY
        else:
            return ELECUSAGEMONTH

    def getResidentById(self, id: str) -> 'Resident':
        for resident in self.residents:
            if resident.id == id:
                return resident

        else:
            raise KeyError("No such resident with that id")