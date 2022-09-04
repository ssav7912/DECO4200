import pigpio
import subprocess

class Location(Enum):
    HOME = 0
    SHOPS = 1
    UNI = 2
    GYM = 3
    WORK = 4

class Resident:
    id: str
    name: str
    location: 'Location' 

    def __init__(id, name):
        self.id = id
        self.name = name
        self.location = Location.HOME


class Board:
    residents: 'set[Resident]'
    url: str


    def __init__():
        self.io = pigpio.pi()

    def __GPIOSetup(pin):
        


if __name__ == "__main__":
    # subprocess.Popen("sudo pigpiod")
    
    
    board = Board()



