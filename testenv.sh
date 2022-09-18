#!/bin/bash

echo Spawning Server
screen -dmS Server python3 -m Web_Portal.server Web_Portal.server

echo Spawning Board
screen -dmS Board python3 -m board.board board.board
