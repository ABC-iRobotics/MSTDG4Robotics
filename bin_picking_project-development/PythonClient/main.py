import sys, os
import platform
import Services.VrepConnector as vcon
import Tasks.BinPickingScene as bps
import Tasks.PegTransferScene as pts
import Query.generateYoloData as genYolo

#1th argument: Selected task ['BinPicking' / 'PegTransfer']
#2th argument: Desired number of training data
#3rd argument: Simulation speed
#4th argument: Mesh filename
#5th argument: Desired number of objects
#6th argument: Table name
#7th argument: Vision sensor name
#8th argument: Bin name
#9th argument: Scaling of inserted object
#10th argument: Vision sensor position in height

#suggested values: BinPicking 10 3 OE_logo_3D.stl 5 Table Vision_sensor Bin 0.006 1.65

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
            binPickingScene.Init(sys.argv[6], sys.argv[7], sys.argv[8], float(sys.argv[9]), float(sys.argv[10]))
            for dbCount in range(datasetCount):
                binPickingScene.Step()
            genYolo.Generate()

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