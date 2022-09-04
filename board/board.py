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

    def move_location(location: 'Location') -> bool:
        if location is self.location:
            return False
        else:
            self.location = location
            #invoke movement?
            return True


class Board:
    residents: 'set[Resident]'
    url: str


    def __init__():
        self.io = pigpio.pi()

        


if __name__ == "__main__":
    # subprocess.Popen("sudo pigpiod")
    
    
    board = Board()



