import sys, os
sys.path.insert(0, os.path.dirname(__file__) + '/Services')
sys.path.insert(0, os.path.dirname(__file__) + '/DataEntities')

import VrepMeshDrawer as vdrawer
import VrepSceneManipulator as sceneMan

import TrainingImage as TI
import Fixture as F
import MongoScv as MS 

elementsCount = 2

def main():
    drawer = vdrawer.VrepMeshDrawer()
    manipulator = sceneMan.VrepSceneManipulator()
    drawer.vrepConn.start()
    
    for i in range(elementsCount):
        drawer.DrawMesh()
    success, objectIds = manipulator.GetObjects('Shape', elementsCount)
    if success is not -1:
        manipulator.SetObjectsToDynamic('Shape', objectIds)
    else:
        print('Error while get inserted object shapes from simulation.')
    manipulator.RePaintElement('customizableTable_tableTop', True)
    path = manipulator.GetImage('Vision_sensor')
    
    mongoDb = MS.MongoService()

    GetPropertiesOfScreenObjects(manipulator, path, mongoDb)


    drawer.vrepConn.stop()
    return 0

def GetPropertiesOfScreenObjects(manipulator, path, mongoDb):
    trainingImage = TI.TrainingImage(path)
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