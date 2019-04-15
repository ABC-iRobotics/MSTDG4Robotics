import sys, os
sys.path.insert(0, os.path.dirname(__file__) + '/libraries')
import ctypes
import vrep

class VrepConnector:
    #host: string, port: int
    def __init__(self, host = '127.0.0.1', port = 19999):
        print ('Program started')
        self.vrep=vrep
        vrep.simxFinish(-1)
        self.clientID=vrep.simxStart(host, port, True, True, 5000, 5)
        if self.clientID!=-1:
            print ('Connected to remote API server')
        else:
            print ('Failed to connect to remote API server')
    
    def callScript(self, functionName, scriptDescription, inInts=[], inFloats=[], inStrings=[], inBuffer=bytearray()):
        res,retInts,retFloats,retStrings,retBuffer =vrep.simxCallScriptFunction(self.clientID, scriptDescription, vrep.sim_scripttype_childscript, functionName, inInts, inFloats, inStrings, inBuffer, vrep.simx_opmode_blocking)
        if res==vrep.simx_return_ok:
            print('Remote function call succeed')
        else:
            print ('Remote function call failed')
        return res,retInts,retFloats,retStrings,retBuffer