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
        self.residents = set()
        self.manifest = set()
        self.url = url

    '''
    Sends a GET to the info server to get the resident manifest.
    If any new ids are found it will ask for their object definitions too
    '''
    def AskForUpdate(self) -> None:
        ids = GetManifest()


        for id in ids:
            if id not in self.manifest:
                newResident = Resident(id, "placeholder")        
                #TODO: Invoke a second request for name & location data
                self.residents.add(newResident)

        self.manifest.update(ids)


        



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


if __name__ == "__main__":
    # subprocess.Popen("sudo pigpiod")
        
    
    board = Board(URL)

    board.AskForUpdate()

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




