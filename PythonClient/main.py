import sys, os
import platform
import Services.VrepConnector as vcon
import Tasks.BinPickingScene as bps
import Tasks.PegTransferScene as pts

#1th argument: V-REP path
#2th argument: Task name
#3th argument: Dataset count
#4th argument: Simulation speed
def main():
    
    selectedTask = 'BinPicking'

    datasetCount = 10
    
    simSpeed = 1
    
    if len(sys.argv) > 1:
        selectedTask = sys.argv[1]
    if len(sys.argv) > 2:
        datasetCount = int(sys.argv[2])
    if len(sys.argv) > 3:
        simSpeed = int(sys.argv[3])
    
    vrepConn = vcon.VrepConnector()

    if vrepConn.connectionWasSuccesfull:    
        vrepConn.start()
        vrepConn.SetSimulationSpeed(simSpeed) #value can set from -3 (0.1x speed) to +6 (64x speed)

        #Logic starts here
        #-----------------
        if selectedTask == 'BinPicking':
            binPickingScene = bps.BinPickingScene(vrepConn, sys.argv[4], int(sys.argv[5]))
            binPickingScene.Init(sys.argv[6], sys.argv[7], sys.argv[8])
            for dbCount in range(datasetCount):
                binPickingScene.Step()

        elif selectedTask == 'PegTransfer':
            pegTransferScene = pts.PegTransferScene(vrepConn, sys.argv[4])
            pegTransferScene.Init(sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
            for dbCount in range(datasetCount):
                pegTransferScene.Step()
            pegTransferScene.SaveBaseData()

        #-----------------
        #Logic ends here

        simSpeed = vrepConn.GetSimulationSpeed()
        vrepConn.stop()
    return 0


if __name__ == "__main__":
    main()