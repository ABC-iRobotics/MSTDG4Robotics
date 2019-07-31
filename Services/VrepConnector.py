import sys, os
import ctypes
import libraries.vrep as vrep
import libraries.vrepConst as vrepConst

class VrepConnector:
    #host: string, port: int
    scriptDescription='remoteApiCommandServer'
    def __init__(self, host = '127.0.0.1', port = 19997):
        print ('Program started')
        self.vrep = vrep
        self.vrepConst = vrepConst
        vrep.simxFinish(-1)
        self.clientID=vrep.simxStart(host, port, True, True, 5000, 5)
        if self.clientID!=-1:
            print ('Connected to remote API server')
        else:
            print ('Failed to connect to remote API server')
    
    def callScript(self, functionName, inInts=[], inFloats=[], inStrings=[], inBuffer=bytearray()):
        res,retInts,retFloats, retStrings,retBuffer =self.vrep.simxCallScriptFunction(self.clientID, self.scriptDescription, vrepConst.sim_scripttype_childscript, functionName, inInts, inFloats, inStrings, inBuffer, vrepConst.simx_opmode_blocking)
        if res == vrepConst.simx_return_ok:
            print('Remote function call succeed')
        else:
            print ('Remote function call failed')
        return res,retInts,retFloats,retStrings,retBuffer

    def start(self):
        self.vrep.simxStartSimulation(self.clientID,vrepConst.simx_opmode_oneshot_wait)
        
    def stop(self):
        self.vrep.simxStartSimulation(self.clientID,vrepConst.simx_opmode_oneshot_wait)

    def finish(self):
        vrep.simxFinish(self.clientID)