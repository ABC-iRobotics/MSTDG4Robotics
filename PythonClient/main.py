import sys, os

import Services.VrepConnector as vcon
import Services.BinPickingScene as bps

def main():
    vrepConn = vcon.VrepConnector()
    if vrepConn.connectionWasSuccesfull:
        #Parameters: 
        #   VrepConnector, 
        #   table name, 
        #   bin name, 
        #   vision sensor name, 
        #   how many part will be appeared, 
        #   how many data should be generated
        binPickingScene = bps.BinPickingScene(vrepConn, 'Table', 'Bin', 'Vision_sensor', 20, 2)

        vrepConn.start()
        vrepConn.SetSimulationSpeed(1) #value can set from -3 (0.1x speed) to +6 (64x speed)
        simSpeed = vrepConn.GetSimulationSpeed()

        binPickingScene.StartLoop()
    
        vrepConn.stop()
    return 0


if __name__ == "__main__":
    main()