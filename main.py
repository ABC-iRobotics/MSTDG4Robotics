import sys, os

import Services.VrepMeshDrawer as vdrawer
import Services.VrepSceneManipulator as sceneMan

import DataEntities.TrainingImage as TI
import DataEntities.Fixture as F
import MongoScv as MS 

elementsCount = 5

def main():
    drawer = vdrawer.VrepMeshDrawer()
    manipulator = sceneMan.VrepSceneManipulator()
    #drawer.vrepConn.start()
    
    for i in range(elementsCount):
        drawer.DrawMesh()
    success, objectIds = manipulator.GetObjects('Shape', elementsCount)
    if success is not -1:
        manipulator.SetObjectsToDynamic('Shape', objectIds)
    else:
        print('Error while get inserted object shapes from simulation.')
    manipulator.RePaintElement('customizableTable_tableTop', True)
    path, deptBuffer, deptResolution = manipulator.GetImage('Vision_sensor')
    
    mongoDb = MS.MongoService()

    GetPropertiesOfScreenObjects(path, deptBuffer, deptResolution, manipulator, mongoDb)


    #drawer.vrepConn.stop()
    #return

def GetPropertiesOfScreenObjects(path, deptBuffer, deptResolution, manipulator,  mongoDb):
    trainingImage = TI.TrainingImage(path, deptBuffer, deptResolution)
    for i in range(elementsCount):
        shapeName = ''
        if i == 0:
            shapeName = 'Shape'
        else:
            shapeName = 'Shape'+str(i-1)
        position_rel, orienatation_rel = manipulator.GetObjectPositionAndOrientation(shapeName, 'Vision_sensor')
        position_abs, orientation_abs = manipulator.GetObjectPositionAndOrientation(shapeName, None)
        trainingImage.addFixtureByParams(position_abs, orientation_abs, position_rel, orienatation_rel)
        
    mongoDb.insert(trainingImage.dictMapper())

if __name__ == "__main__":
    main()