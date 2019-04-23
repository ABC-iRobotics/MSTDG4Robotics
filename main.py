import sys
import VrepMeshDrawer as vdrawer
import VrepSceneManipulator as sceneMan

elementsCount = 10

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
    manipulator.GetImage('binCam')
    
    drawer.vrepConn.stop()
    return 0

if __name__ == "__main__":
    main()