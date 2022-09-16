from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, HTTPServer
import time
import os
import json 
from core.STScorelib import Resident, Location, ResidentDecoder
from urllib import parse


hostName = "localhost"
serverPort = 8080


class MyServer(SimpleHTTPRequestHandler):
    '''
    API Interface:

    GET:

    When `query?manifest=true` will return a list of the current userids stored

    When `query?id=[<id>]` will return the location of the given userid. 

    PUT:
    Takes in a JSON object describing a `Resident` class and stores it.
    '''
    manifest: 'set(Resident)' = {Resident("abc", "soren")}   
    
    
    def do_GET(self):

        request = parse.parse_qs(parse.urlparse(self.path).query)

        wantmanifest = request.get("manifest")
        queryids = request.get("id")
        
        # print(request.get("manifest"))
        if wantmanifest is not None and queryids is None:
            if wantmanifest[0] == "true":
                response = self.returnManifest()
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(response.encode('utf8'))
            else:
                self.send_response(400, "Invalid request")
        
        elif wantmanifest is None and queryids is not None:
            response = self.returnLocations(queryids)

            if response is None:
                self.send_response(400, "No such id")
            else: 
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(response.encode('utf8'))



        else:
            super().do_GET()


    
    def returnManifest(self) -> str:
        manifest = [elem.id for elem in self.manifest]

        return json.dumps(manifest)

    def returnLocations(self, queryids: 'list[str]') -> str:
        locations = []
        for id in queryids:
            try:
                resident = self.getResidentById(id)
                locations.append(str(resident.location))
            except:
                pass

        if len(locations) == 0:
            return None

        return json.dumps(locations)


    def getResidentById(self, id: str) -> 'Resident':
        for resident in self.manifest:
            if resident.id == id:
                return resident
        else:
            raise KeyError("No such resident with that id")


    def do_PUT(self):
        
        filename = os.path.basename(self.path)
        print(filename)

        file_length = int(self.headers['Content-Length'])
        print(self.rfile.read(file_length))
        
        try:
            person = json.loads(self.rfile.read(file_length), cls=ResidentDecoder)
        except json.JSONDecodeError as j:
            print(j.msg)
            self.send_response(400, "Not a valid JSON object")
            self.end_headers()
            self.wfile.write("Error")
            return

        self.manifest.add(person)
        print(self.manifest)

        self.send_response(204)
        self.end_headers()
        self.wfile.write("Saved".encode('utf8'))

        # with open(f"current/{filename}", 'wb') as output_file:
        #     output_file.write(person.toJson())
        #     self.send_response(204, 'Created!')
        #     self.end_headers()
        #     # reply_body = "Saved"
        #     # self.wfile.write(reply_body.encode('utf8'))

    


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)

    print("Server Started")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Stopped")