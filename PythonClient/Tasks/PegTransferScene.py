import Services.VrepObject as vo
import Services.VrepSceneDrawer as vdrawer
import Services.VrepSceneManipulator as sceneMan

import DataEntities.TrainingImage as TI
import DataEntities.BaseData as BD
import DataEntities.Fixture as F
import Services.MongoScv as MS 
import Helper as hp
import uuid

class PegTransferScene:

    def __init__(self, vrepConnector, meshPath):
        self.vrepConn = vrepConnector
        self.helper = hp.Helper()
        self.taskName = 'PegTransfer'
        
        self.drawer = vdrawer.VrepSceneDrawer(vrepConnector, self.taskName)

        self.manipulator = sceneMan.VrepSceneManipulator(vrepConnector, self)
        self.mongoDb = MS.MongoService(self.taskName)
        self.mongoDbBase = MS.MongoService(self.taskName+'Base')

        self.meshPath = meshPath


    def Init(self, surfaceName, spotlight, visionSensor, cylinderName):
        self.surface = vo.VrepObject(self.vrepConn, surfaceName)
        self.visionSensor = vo.VrepObject(self.vrepConn, visionSensor)
        self.guid = str(uuid.uuid4())
        self.fixtures = [] 
        self.lights = self.manipulator.GetObjectList(spotlight, 1)
        self.cylinders = self.manipulator.GetObjectList(cylinderName, 1)
        self.SaveBaseData()
        
    def Step(self):
        count = self.helper.GetRandom(1, len(self.cylinders), False)
        randomHistoryList = []
        for i in range(count):
            random = self.helper.GetRandom(0, (len(self.cylinders)-1), False)
            while random in randomHistoryList or len(randomHistoryList) > 12:
                random = self.helper.GetRandom(1, (len(self.cylinders)-1), False)
            if len(randomHistoryList) < 13:
                randomHistoryList.append(random)
                position, orientation = self.cylinders[random].GetObjectPositionAndOrientation()
                position[1] = position[1] + 0.004
                self.drawer.DrawMesh(self.meshPath, 1, [1, 1, 1], position, orientation)
                if i == 0:
                    self.fixtures.append(vo.VrepObject(self.vrepConn, "Shape"))
                else:
                    self.fixtures.append(vo.VrepObject(self.vrepConn, ("Shape"+ str(i-1))))
                self.fixtures[-1].SetTransparency(0.7)

        imgPath, deptPath, resolution = self.manipulator.GetImage(self.visionSensor.name)
            
        self.GetPropertiesOfScreenObjects(imgPath, deptPath, resolution)
        
        self.DeleteCreatedObjects()
        print('Test')
        
    def GetPropertiesOfScreenObjects(self, path, deptBuffer, deptResolution):
        trainingImage = TI.TrainingImage(path, deptBuffer, deptResolution, self.guid)

        for element in self.fixtures:
            position_rel, orienatation_rel = element.GetObjectPositionAndOrientation(self.visionSensor.name)
            position_abs, orientation_abs = element.GetObjectPositionAndOrientation(None)
            trainingImage.addFixtureByParams(position_abs, orientation_abs, position_rel, orienatation_rel)

        self.mongoDb.insert(trainingImage.dictMapper())

    def DeleteCreatedObjects(self):
        self.RemoveAllShapes()
    
    def RemoveAllShapes(self):
        for element in self.fixtures:
            element.Remove()
        self.fixtures = []
    
    def SaveBaseData(self):
        data = BD.BaseData(self.guid)

        for element in self.cylinders:
            position_rel, orienatation_rel = element.GetObjectPositionAndOrientation(self.visionSensor.name)
            position_abs, orientation_abs = element.GetObjectPositionAndOrientation(None)
            data.addFixtureByParams(position_abs, orientation_abs, position_rel, orienatation_rel)

        self.mongoDbBase.insert(data.dictMapper('pegs'))