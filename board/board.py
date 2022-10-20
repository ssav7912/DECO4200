import eel
import os
import requests
from core.STScorelib import *
import time
import datetime
import numpy as np
from random import random
import sys


class Board:
    '''
    Board controller class.
    '''
    manifest: 'set[str]'
    residents: 'list[Resident]'
    url: str
    home: 'Home'

    @eel.expose
    def __init__(self, url, debug: 'bool' = False):
        self.residents = []
        self.manifest = set()
        self.url = url
        self.home = None

        eel.init('board/web')

        if debug:
            self.residents = [x for x in DEBUGMANIFEST]                


    def newHome(self, name: str, numlights: int):
        self.home = Home(name, numlights)
        self.home.appliances = DEBUGAPPLIANCES
        self.home.togglelight(0, True)
        self.home.togglelight(2, True)
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
                eel.CreateResidentCardWrapper(resident.toJson())
            else:
                self.residents[self.residents.index(self.getResidentById(id))] = resident
                eel.updateResidentWrapper(location)
                                

        self.manifest.update(ids)

    def AskForUsers(self) -> None:
        users = getUsers()

        for i, user in enumerate(users):
            if user.id not in self.manifest:
                self.manifest.add(user.id)
                self.residents.append(user)
                eel.CreateResidentCardWrapper(user.toJson())
            else:
                self.residents[self.residents.index(self.getResidentById(user.id))] = user
                eel.updateResidentWrapper(user.toJson())
        
    

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

def getUsers() -> 'set[Resident]':
    userRequest = requests.get(URL, params={"users": "true"})
    print(userRequest.url)

    # try:
    lis = userRequest.json()
    users = set()
    for obj in lis:
        resident = json.loads(obj, cls=ResidentDecoder)
        users.add(resident)
            

    # except:
    #     print("User object incorrect!")
    #     users = set()
    
    return users
    
@eel.expose
def getName() -> 'str':
    nameRequest = requests.get(URL, params={"homename": "true"})
    
    name = nameRequest.text

    print(name)

    return name


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
    eel.expose(board.home.getAppliances)
    # eel.generateResidents(board.getResidents())

    if len(sys.argv) == 2:
        hostname = sys.argv[1]
    
    else:
        hostname = "localhost"
    

            
    eel.start('index.html', mode=None, block=False)
    try:

        board.AskForUsers()
    except requests.exceptions.ConnectionError:
        print("Awaiting Connection...")

    while True:
        try:

            eel.sleep(5)
        
        
            try:
                board.AskForUsers()
                print(board.residents)
            

            except requests.exceptions.ConnectionError: 
                print("Awaiting Connection...")
                pass
        
        except KeyboardInterrupt:
            break


