# DECO4200
Team repository for DECO4200

This repository stores the source programs for the HouseHub proof of concept interface.

There are 2 main components:
- The Board (`board` directory)
- The Server (`Web_Portal` directory)

Common library utils and resources are stored in `core`. Both the board and the server depend on this.

## The Board
The board handles management of the chalkboard display UI, as well as any other 'household' tasks, such as communicating with Smart Meter APIs. The board communicates with the Server to retrieve information about the household members. Ideally, Smart Meter interactions (currently unimplemented) should be handled by the board, separate to any central server communication.


## The Server
The server hosts a mobile web-interface and an HTTP API to send and retrieve information about the household. Through the web-interface, users can update their status to the household from anywhere with an internet connection. 

The server supports the following HTTP requests:
### GET:

When `query?manifest=true` will return a list of the current userids stored.

When `query?id=[<id>]` will return the given userid object as a JSON string.

When `query?users=true` will return a list of all user objects (in JSON).

When `query?homename=true` will return the current household name.

### PUT:
Takes in a JSON object describing a `Resident` class and stores it if the name doesn't match any stored, or overwrites that record if it does.

```json
{
    "name": str,
    "id": str,
    "location": str(Location),
    "status": str(Status),
    "statstring": str
    "emoji": str

}
 ``` 

## Hardware Requirements
Minimum requirements for the device are:
- Hardware to run the server from
- Hardware to run the board from
- An ipad-sized display to render the board UI
- A mobile device to access the web interface.

The hardware will need some OS, and will need an internet connection. For this project, we used a Raspberry Pi to host both the board and server processes from, in a sandboxed local wireless network broadcast via the RPi. However, the system is designed so that the board and server can be hosted separately: the board on the users local (private) network, and the server on some public host. This is the ideal use case, as residents would be able to update their status independent of their local network. 


## Install and Running
Dependencies:
- Python 3.8 or above and the standard library.
- Eel
- NumPy
- Requests
  
These packages are all available via `pip`

The repository provides a script `testenv.sh` to start up both the Board and the Server on a local machine. This just spawns both processes in named `screen` terminals:
```bash
screen -dMS Server python3 -m Web_Portal.server Web_Portal.server
screen -dMS Board python3 -m board.board board.board
```
By default, the server spawns a page on `http://localhost:8080`. The board will listen on `localhost` for HTTP API requests, and it will spawn its own interface on `http://localhost:8000`. Neither of these are secured with HTTPS, so do not send any sensitive data over this system.

One can view debug output from either screen session with `screen -Dr [Session Name]`. See the `screen` manual for more information.
