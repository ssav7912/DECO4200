import eel
import requests
from core.STScorelib import Resident, Location, Appliance
import time
import datetime
import numpy as np
from random import random

#sample electricty usage datasets
ELECUSAGEMONTH: 'np.ndarray' = np.interp([np.random.random() for x in range(30)], [0, 1], [20, 25]) 
ELECUSAGEDAY: 'np.ndarray' = np.interp([np.random.random() for x in range(24)], [0, 1], [0, 1])

class Board:
    '''
    Board controller class.
    '''
    manifest: 'set[str]'
    residents: 'list[Resident]'
    appliances: 'list[Appliance]'
    url: str


    def __init__(self, url, debug: 'bool' = True):
        self.residents = []
        self.manifest = set()
        self.url = url
        self.appliances = []

        eel.init('web')

        if debug:
            eel.start('UI.html', mode=None)
        else: 
            eel.start('UI.html')

    '''
    Sends a GET to the info server to get the resident manifest.
    If any new ids are found it will ask for their object definitions too
    '''
    def AskForUpdate(self) -> None:
        ids = GetManifest()

        updates = list(ids)
        locations = getLocations(updates)

        for i, (id, location) in enumerate(zip(updates, locations)):
            if id not in self.manifest:
                self.manifest.add(id)
                resident = Resident(id, "placeholder")
                self.residents.append(resident)

            elif id in self.manifest:
                resident = self.getResidentById(id)
                                

        self.manifest.update(ids)


    def getResidentById(self, id: str) -> 'Resident':
        for resident in self.residents:
            if resident.id == id:
                return resident

        else:
            raise KeyError("No such resident with that id")

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
        

        return np.array([1, 2, 3])

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
    board = Board(URL)

    board.AskForUpdate()

    while True:
        try:

            time.sleep(5)
        
        
            try:
                board.AskForUpdate()
                print(board.residents)
            

            except requests.exceptions.ConnectionError: 
                print("Awaiting Connection...")
                pass
        
        except KeyboardInterrupt:
            break


