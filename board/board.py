import eel
import os
import requests
from core.STScorelib import *
import time
import datetime
import numpy as np
from random import random

class Board:
    '''
    Board controller class.
    '''
    manifest: 'set[str]'
    residents: 'list[Resident]'
    url: str
    home: 'Home'

    @eel.expose
    def __init__(self, url, debug: 'bool' = True):
        self.residents = []
        self.manifest = set()
        self.url = url
        self.home = None

        eel.init('board/web')

        if debug:
            self.residents = [Resident(x, x) for x in ["Soren", "Trang", "David", "Sajitha"]]                


    def newHome(self, name: str, numlights: int):
        self.home = Home(name, numlights)
        data = self.home.querySmartMeter(datetime.datetime(2022,10,1), datetime.datetime(2022,10,30))
        print("send")
        # eel.newConsumptionPlot([x for x in range(1, 30)], list(data))
        return None

    def getData(self, utility: 'str'):
        if utility == 'ELECTRICITY': 
            data = self.home.querySmartMeter(datetime.datetime(2022,10,1), datetime.datetime(2022,10,30))
        elif utility == 'WATER':
            data = self.home.queryWaterUsage(datetime.datetime(2022,10,1), datetime.datetime(2022,10,30))
        elif utility == 'GAS':
            data = self.home.queryGasUsage(datetime.datetime(2022,10,1), datetime.datetime(2022,10,30))
        
        return [list(data), [x for x in range(1, 30)]]

    def getLights(self) -> int:
        return self.home.getLightsOn()

    def getResidents(self):
        obj = [x.toJson() for x in self.residents]
        return obj

    '''
    Sends a GET to the info server to get the resident manifest.
    If any new ids are found it will ask for their object definitions too
    '''
    def AskForUpdate(self) -> None:
        ids = GetManifest()

        updates = list(ids)
        locations = getLocations(updates)
        print(locations)

        for i, (id, location) in enumerate(zip(updates, locations)):
            resident = json.loads(location, cls=ResidentDecoder)
          
            if id not in self.manifest:
                self.manifest.add(id)
                self.residents.append(resident)
            else:
                self.residents[self.residents.index(self.getResidentById(id))] = resident
                eel.updateResidentWrapper(location)
                                

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
    board = Board(URL)

    board.newHome("test", 4)
    eel.expose(board.getData)
    eel.expose(board.getResidents)
    eel.expose(board.getLights)
    # eel.generateResidents(board.getResidents())


            
    eel.start('index.html', mode=None, block=False)
    
    board.AskForUpdate()

    while True:
        try:

            eel.sleep(5)
        
        
            try:
                board.AskForUpdate()
                print(board.residents)
            

            except requests.exceptions.ConnectionError: 
                print("Awaiting Connection...")
                pass
        
        except KeyboardInterrupt:
            break


