#!/bin/bash

echo Spawning Server
screen -mS Server python3 Web_Portal/server.py

echo Spawning Board
screen -mS Board python3 board/board.py
