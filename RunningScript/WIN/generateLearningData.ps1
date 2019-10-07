param($vrepPath="C:/Program Files/V-REP3/V-REP_PRO_EDU")
pwd
start-job -scriptblock {
	& $vrepPath/vrep.exe -h -s -q ./../../PythonClient/vrep_scenes/binPicking.ttt
}
start-job -scriptblock{
	C:\MongoDB\bin\mongod.exe
}
sleep 5

#& python ./../../PythonClient/main.py