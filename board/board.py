# import pigpio
import subprocess
import asyncio
import requests
from core.STScorelib import Resident, Location


class Board:
    '''
    Board controller class.
    '''
    manifest: 'set[str]'
    residents: 'set[Resident]'
    url: str


    def __init__(self, url):
        # self.io = pigpio.pi()
        self.residents: 'set[Resident]' = set()
        self.manifest = set()
        self.url = url

    '''
    Sends a GET to the info server to get the resident manifest.
    If any new ids are found it will ask for their object definitions too
    '''
    def AskForUpdate(self) -> None:
        ids = GetManifest()

        updates = list(ids)
        locations = getLocations(updates)

        for id, location in zip(updates, locations):
            if id not in self.manifest:
                self.manifest.add(id)
                resident = Resident(id, "placeholder")
                resident.location = Location.fromString(location)
                self.residents.add(resident)

            elif id in self.manifest:
                resident = self.getResidentById(id)
                resident.location = Location.fromString(location)
                

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
        
    
    board = Board(URL)

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




