import Services.VrepObject as vo
import Services.VrepSceneDrawer as vdrawer
import Services.VrepSceneManipulator as sceneMan

import DataEntities.TrainingImage as TI
import DataEntities.Fixture as F
import Services.MongoScv as MS 

class PegTransferScene:

    def __init__(self, vrepConnector, meshPath):
        self.vrepConn = vrepConnector
        self.drawer = vdrawer.VrepSceneDrawer(vrepConnector, self)

        self.manipulator = sceneMan.VrepSceneManipulator(vrepConnector, self)
        self.mongoDb = MS.MongoService('PegTransfer')

        self.meshPath = meshPath


    def Init(self, surfaceName, pegName, visionSensor, lights, cylinders):
        self.surface = vo.VrepObject(self.vrepConn, surfaceName)
        self.visionSensor = vo.VrepObject(self.vrepConn, visionSensor)

        self.pegs = [] 
        self.lights = []
        self.cylinders = []

        self.pegs.append(vo.VrepObject(self.vrepConn, pegName))
        for elem in lights:
            self.lights.append(vo.VrepObject(self.vrepConn, elem))
        for elem in cylinders:
            self.cylinders.append(vo.VrepObject(self.vrepConn, elem))

    def Step(self):
        print('Test')
        