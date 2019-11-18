#!/bin/bash 
VREP_NAME=$1
/Applications/$VREP_NAME/vrep.app/Contents/MacOS/vrep -h -s -q `pwd`/vrep_scenes/binPicking.ttt &
mongod &
sleep 5
python3 ./../../PythonClient/main.py