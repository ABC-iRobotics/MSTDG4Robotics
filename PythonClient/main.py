import sys, os

import Services.VrepConnector as vcon
import Tasks.BinPickingScene as bps
import Tasks.PegTransferScene as pts

def main():
    datasetCount = int(sys.argv[1])
    if datasetCount is None:
        datasetCount = 2

    meshCount = int(sys.argv[2])
    if meshCount is None:
        meshCount = 20
    meshName = sys.argv[3]
    simulationSpeed = 1
    vrepConn = vcon.VrepConnector()
    
    if vrepConn.connectionWasSuccesfull:    
        vrepConn.start()
        vrepConn.SetSimulationSpeed(simulationSpeed) #value can set from -3 (0.1x speed) to +6 (64x speed)

        #Logic starts here
        #-----------------
        
        binPickingScene = bps.BinPickingScene(vrepConn, 'Table', 'Bin', 'Vision_sensor', meshName, meshCount, datasetCount)
        for dbCount in range(datasetCount):
            binPickingScene.Step()
        
        pegTransferScene = pts.PegTransferScene(vrepConn, meshName)
        pegTransferScene.Init('Surface', 'PEG', 'Vision_sensor', 
            [
                'Spotlight1',
                'Spotlight2',
                'Spotlight3',
                'Spotlight4'
            ], 
            [
                'Cylinger1_1',
                'Cylinger1_2',
                'Cylinger1_3',
                'Cylinger2_1',
                'Cylinger2_2',
                'Cylinger2_3',
                'Cylinger3_1',
                'Cylinger3_2',
                'Cylinger4_1',
                'Cylinger4_2',
                'Cylinger5_1',
                'Cylinger5_2',
            ])
        for dbCount in range(datasetCount):
            pegTransferScene.Step()
            
        #-----------------
        #Logic ends here

        simSpeed = vrepConn.GetSimulationSpeed()
        vrepConn.stop()
    return 0


if __name__ == "__main__":
    main()