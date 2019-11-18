import Services.VrepObject as vo
import Services.VrepSceneDrawer as vdrawer
import Services.VrepSceneManipulator as sceneMan

import DataEntities.TrainingImage as TI
import DataEntities.Fixture as F
import Services.MongoScv as MS 
import Helper as hp

class PegTransferScene:

    def __init__(self, vrepConnector, meshPath):
        self.vrepConn = vrepConnector
        self.helper = hp.Helper()
        self.taskName = 'PegTransfer'
        self.drawer = vdrawer.VrepSceneDrawer(vrepConnector, self.taskName)

        self.manipulator = sceneMan.VrepSceneManipulator(vrepConnector, self)
        self.mongoDb = MS.MongoService(self.taskName)

        self.meshPath = meshPath


    def Init(self, surfaceName, pegName, visionSensor, lightName, cylinderName):
        self.surface = vo.VrepObject(self.vrepConn, surfaceName)
        self.visionSensor = vo.VrepObject(self.vrepConn, visionSensor)

        self.pegs = [vo.VrepObject(self.vrepConn, pegName)] 
        self.lights = self.manipulator.GetObjectList(lightName, 1)
        self.cylinders = self.manipulator.GetObjectList(cylinderName, 1)
        
    def Step(self):
        count = self.helper.GetRandom(1, len(self.cylinders), False)
        for i in range(count):
            random = self.helper.GetRandom(1, (len(self.cylinders)-1), False)
            position, orientation = self.cylinders[random].GetObjectPositionAndOrientation()
            position[1] = position[1] + 0.004
            self.drawer.DrawMesh(self.meshPath, 1, [1, 1, 1, 0.3], position, orientation)
            if i is 0:
                self.pegs.append(vo.VrepObject(self.vrepConn, "Shape"))
            else:
                self.pegs.append(vo.VrepObject(self.vrepConn, ("Shape"+ str(i-1))))

        print('Test')
        