import pigpio
import subprocess
import asyncio
import requests
from core.STScorelib import Resident, Location
import argparse


class Board:
    '''
    Board controller class.
    '''
    manifest: 'set[str]'
    residents: 'list[Resident]'
    url: str


    def __init__(self, url):
        self.io = pigpio.pi()
        self.pioinit([2, 3])
        self.residents: 'set[Resident]' = []
        self.manifest = set()
        self.url = url
        self.mapping = self.initpinstruct()
        


    #Pin mapping:
    #Resident 1:
    #   - HOME -> 2
    #   - WORK ->
    #Resident 2:
    #    - HOME -> 3
    def initpinstruct(self) {
        # mapping = {resident: {Location.HOME:None, Location.SHOPS: None, Location.WORK: None, Location.GYM: None} for resident in self.residents}
        mapping = {
            1: {Location.HOME:2, Location.SHOPS: None, Location.WORK: None, Location.GYM: None},
            2: {Location.HOME:3, Location.SHOPS: None, Location.WORK: None, Location.GYM: None}
        }
        return mapping

    }

    def pioinit(self, outputpins: 'list[int]') -> None:
        self.outputpins = outputpins
        
        for pin in outputpins:
            self.io.set_mode(pin, pigpio.OUTPUT)
            self.io.write(pin, 0)

    def move_location(self, resident, newLocation: 'Location') -> None:
        oldpin = self.mapping[self.residents.index(resident)][resident.location]

        self.io.write(oldpin, 0)

        resident.location = newLocation

        newpin = self.mapping[self.residents.index(resident)][resident.location]
        
        self.io.write(newpin, 1)


    '''
    Sends a GET to the info server to get the resident manifest.
    If any new ids are found it will ask for their object definitions too
    '''
    def AskForUpdate(self) -> None:
        ids = GetManifest()

        updates = list(ids)
        locations = getLocations(updates)

        for i, id, location in enumerate(zip(updates, locations)):
            if id not in self.manifest:
                self.manifest.add(id)
                resident = Resident(id, "placeholder")
                self.move_location(self.getResidentById(id), Location.fromString(location))
                self.residents.append(resident)

            elif id in self.manifest:
                resident = self.getResidentById(id)
                
                self.move_location(self.getResidentById(id), Location.fromString(location))
                

        self.manifest.update(ids)


    def getResidentById(self, id: str) -> 'Resident':
        for resident in self.residents:
            if resident.id == id:
                return resident

        else:
            raise KeyError("No such resident with that id")


        

URL = "http://localhost:8080/"

def GetManifest() -> 'set[str]':
    manifestrequest = requests.get(URL, params={"manifest": "true"})
    print(manifestrequest.url)


    try:
        manifest = manifestrequest.json()
    except:
        print("Manifest object was incorrect!")
        manifest = set()

    return set(manifest)

def getLocations(ids: 'list[str]') -> 'list[Location]':
    locationrequest = requests.get(URL, params={"id": ids})
    
    try:
        location = locationrequest.json()
    except:
        print("Location object incorrect!")
        return []
    
    return location 

if __name__ == "__main__":
    # subprocess.Popen("sudo pigpiod")
        

    parser = argparse.ArgumentParser(description="board.py [URL] --pins [pins]")

    parser.add_argument('URL', type=str, help="Required URL to receive resident data from")


    args = parser.parse_args()


    
    board = Board(arg.pos_arg[0])

    board.AskForUpdate()
    print(board.residents)

    # loop = asyncio.get_event_loop()
    # try:
    #     asyncio.ensure_future(board.AskForUpdate())
    #     asyncio.sleep(10)
    #     loop.run_forever()
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     print("Shutting down")
    #     loop.close()




