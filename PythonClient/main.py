import sys, os

import Services.VrepMeshDrawer as vdrawer
import Services.VrepSceneManipulator as sceneMan

import DataEntities.TrainingImage as TI
import DataEntities.Fixture as F
import Services.MongoScv as MS 

elementsCount = 10
dbRowToAddCount = 10

def main():
    drawer = vdrawer.VrepMeshDrawer()
    manipulator = sceneMan.VrepSceneManipulator()
    mongoDb = MS.MongoService()
    
    drawer.vrepConn.start()
    manipulator.SetSimulationSpeed(6) #value can set from -3 (0.1x speed) to +6 (64x speed)
    simSpeed = manipulator.GetSimulationSpeed()
    for i in range(dbRowToAddCount):
        DrawMeshes(drawer)

        SetObjectsToDynamic('Shape', manipulator)
        
        manipulator.RePaintElement('customizableTable_tableTop', True)

        imgPath, deptPath, resolution = manipulator.GetImage('Vision_sensor')
        
        GetPropertiesOfScreenObjects(imgPath, deptPath, resolution, 'Shape', manipulator, mongoDb)

        DeleteCreatedObjects('Shape', manipulator)
        
    drawer.vrepConn.stop()
    return 0

def GetPropertiesOfScreenObjects(path, deptBuffer, deptResolution, name, manipulator,  mongoDb):
    trainingImage = TI.TrainingImage(path, deptBuffer, deptResolution)
    for i in range(elementsCount):
        shapeName = ''
        if i == 0:
            shapeName = name
        else:
            shapeName = name+str(i-1)
        position_rel, orienatation_rel = manipulator.GetObjectPositionAndOrientation(shapeName, 'Vision_sensor')
        position_abs, orientation_abs = manipulator.GetObjectPositionAndOrientation(shapeName, None)
        trainingImage.addFixtureByParams(position_abs, orientation_abs, position_rel, orienatation_rel)
        
    mongoDb.insert(trainingImage.dictMapper())

def DrawMeshes(drawer):
    for i in range(elementsCount):
        drawer.DrawMesh()

def SetObjectsToDynamic(name, manipulator):
    success, objectIds = manipulator.GetObjects(name, elementsCount)
    if success is not -1:
        manipulator.SetObjectsToDynamic(name, objectIds)
    else:
        print('Error while get inserted object shapes from simulation.')

def DeleteCreatedObjects(name, manipulator):
    for i in range(elementsCount):
        shapeName = ''
        if i == 0:
            shapeName = name
        else:
            shapeName = name+str(i-1)
        manipulator.RemoveObject(shapeName)

if __name__ == "__main__":
    main()