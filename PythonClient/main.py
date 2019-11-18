import sys, os

import Services.VrepConnector as vcon
import Tasks.BinPickingScene as bps
import Tasks.PegTransferScene as pts

def main():
    datasetCount = 1
    meshCount = 20
    meshName = 'tube.obj'
    if len(sys.argv) > 1:
        datasetCount = int(sys.argv[1])
    if len(sys.argv) > 2:
        meshCount = int(sys.argv[2])
    if len(sys.argv) > 3:
        meshName = sys.argv[3]

    simulationSpeed = 1
    vrepConn = vcon.VrepConnector()
    
    selectedProgram = 'PegTransfer'

    if vrepConn.connectionWasSuccesfull:    
        vrepConn.start()
        vrepConn.SetSimulationSpeed(simulationSpeed) #value can set from -3 (0.1x speed) to +6 (64x speed)

        #Logic starts here
        #-----------------
        if selectedProgram is 'BinPicking':
            binPickingScene = bps.BinPickingScene(vrepConn, 'Table', 'Bin', 'Vision_sensor', meshName, meshCount, datasetCount)
            for dbCount in range(datasetCount):
                binPickingScene.Step()
                
        elif selectedProgram is 'PegTransfer':
            pegTransferScene = pts.PegTransferScene(vrepConn, meshName)
            pegTransferScene.Init('Surface', 'PEG', 'Vision_sensor', 'Spotlight', 'Cylinder')
            for dbCount in range(datasetCount):
                pegTransferScene.Step()
            
        #-----------------
        #Logic ends here

        simSpeed = vrepConn.GetSimulationSpeed()
        vrepConn.stop()
    return 0


if __name__ == "__main__":
    main()