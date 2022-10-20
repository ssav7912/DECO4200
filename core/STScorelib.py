import json
from enum import Enum
import datetime
import time
import numpy as np

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
        return super().__str__().replace("Status.", "")

    
    def jsonrep(self) -> str:
        return super().__str__().replace("Status.", "")

    @staticmethod
    def fromString(string: str) -> 'Status':
        dic = {status.jsonrep() : status for status in Status}
        print(dic, string)
        try:
            return dic[string]
        except KeyError:
            print("Unknown status!")
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
    statstring: str
    emoji: str

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.location = Location.HOME
        self.status = Status.AVAILABLE
        self.statstring = ""
        self.emoji = "😊"

    def __repr__(self) -> 'str':

        return "<ID: " + self.id + " NAME: " + self.name + " LOCATION: " + str(self.location) + " STATUS: " + str(self.status) + ">"

    def move_location(self, location: 'Location') -> bool:
        if location is self.location:
            return False
        else:
            self.location = location
            #invoke movement?
            return True

    def toJson(self):
        dic = {"id": self.id, "name": self.name, "location": str(self.location), "status": str(self.status), "statstring": self.statstring, "emoji": self.emoji}
        # print(dic)
        return json.dumps(dic)


    def overwrite(self, other: 'Resident'):
        self.id = other.id
        self.name = other.name
        self.location = other.location
        self.status = other.status
        self.statstring = other.statstring
        self.emoji = other.emoji

class ResidentDecoder(json.JSONDecoder):
    def decode(self, s: 'str') -> 'Resident':
        obj = json.loads(s)

        fields = {"id", "name", "location", "status", "statstring", "emoji"}

        if any(field not in obj.keys() for field in fields):
            raise json.JSONDecodeError("Not an appropriate Resident object for this decoder", s) 

        resident = Resident(obj["id"], obj["name"])
        resident.location = Location.fromString(obj["location"])
        resident.status = Status.fromString(obj["status"])
        resident.emoji = obj["emoji"]
        resident.statstring = obj["statstring"]
        return resident

class Appliance:
    '''
    Generic Appliance class
    '''
    mode: 'str'
    timestamp: 'datetime.datetime'
    name: 'str'
    timeleft: 'int'

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

    def getTimeLeft(self) -> int:
        if self.mode == "INUSE":
            return self.timeleft
        else:
            return 0

    def toJson(self) -> 'str':
        return {"mode": self.mode, "name": self.name, "timeleft": self.timeleft}

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
        self.init_lights(numlights)
        self.utilities = {x for x in Utility}
    

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

    def getAppliances(self) -> 'list[Appliance]':
        return [x.toJson() for x in self.appliances]
        
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

    def queryWaterUsage(self, pstart: 'datetime.datetime', pend: 'datetime.datetime') -> 'np.ndarray':
        '''
        Unimplemented! Returns Test Data

        Should query some smart meter API to retrieve water usage over the specified time period, returning it as an array.
        '''

        if (abs((pstart - pend)).days) <= 1:
            return WATERUSAGEDAY
        else:
            return WATERUSAGEMONTH

    def queryGasUsage(self, pstart: 'datetime.datetime', pend: 'datetime.datetime') -> 'np.ndarray':
        '''
        Unimplemented! Returns Test Data

        Should query some smart meter API to retrieve gas usage over the specified time period, returning it as an array.        
        '''
        if (abs((pstart- pend)).days) <= 1:
            return GASUSAGEDAY
        else:
            return GASUSAGEMONTH

    def getResidentById(self, id: str) -> 'Resident':
        for resident in self.residents:
            if resident.id == id:
                return resident

        else:
            raise KeyError("No such resident with that id")


ELECUSAGEMONTH: 'np.ndarray' = np.interp([np.random.random() for x in range(30)], [0, 1], [20, 25]) 
ELECUSAGEDAY: 'np.ndarray' = np.interp([np.random.random() for x in range(24)], [0, 1], [0, 1])

WATERUSAGEMONTH: 'np.ndarray' = np.interp([np.random.random() for x in range(30)], [0, 1], [180*3, 220*3])
WATERUSAGEDAY: 'np.ndarray' = np.interp([np.random.random() for x in range(24)], [0,1], [(180*3)/24, (220*3)/24])

GASUSAGEMONTH: 'np.ndarray' = np.interp([np.random.random() for x in range(30)], [0, 1], [20, 23])
GASUSAGEDAY: 'np.ndarray' = np.interp([np.random.random() for x in range(24)], [0, 1], [20/24, 23/24])

DEBUGMANIFEST = [Resident(x,x) for x in ["David", "Trang", "Sajitha", "Callum"]]
DEBUGSTATUS = [Status.AVAILABLE, Status.AWAY, Status.DONOTDISTURB, Status.AVAILABLE]
DEBUGSTATSTRING = ["I'm making coffee", "I'm out at work", "Studying!", ""]
DEBUGEMOJI = ["☕","👨‍💻","📚","😺"]

for index, resident in enumerate(DEBUGMANIFEST):
    resident.status = DEBUGSTATUS[index]
    resident.statstring = DEBUGSTATSTRING[index]
    resident.emoji = DEBUGEMOJI[index] 

DEBUGHOMENAME: 'str' = "DECO4200"

DEBUGAPPLIANCES = [Appliance(x) for x in ["Dishwasher", "Washing Machine", "Dryer"]]
DEBUGTIME = [50, 30, 100]
DEBUGAPPLIANCESTATUS = ["INUSE", "INUSE", "AVAILABLE"]
for index, appliance in enumerate(DEBUGAPPLIANCES):
    appliance.timeleft = DEBUGTIME[index]
    appliance.mode = DEBUGAPPLIANCESTATUS[index]