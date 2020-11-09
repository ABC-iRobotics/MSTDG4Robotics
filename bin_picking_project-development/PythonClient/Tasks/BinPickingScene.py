import uuid

import Services.VrepObject as vo
import Services.VrepSceneDrawer as vdrawer
import Services.VrepSceneManipulator as sceneMan
import Services.VrepConnector as vcon
import DataEntities.TrainingImage as TI
import DataEntities.Fixture as F
import Services.MongoScv as MS 
import time #DGU - 09.20
class BinPickingScene:

        #Parameters: 
        #   VrepConnector, 
        #   table name, 
        #   bin name, 
        #   vision sensor name, 
        #   how many part will be appeared, 
        #   how many data(image) should be generated

    def __init__(self, vrepConnector, meshName = None, elementsCount = 20):
        
        self.vrepConn = vrepConnector
        self.drawer = vdrawer.VrepSceneDrawer(vrepConnector)
        self.manipulator = sceneMan.VrepSceneManipulator(vrepConnector, self)
        self.mongoDb = MS.MongoService('BinPicking')
        self.elementsCount = elementsCount
        self.meshName = meshName
        self.guid = str(uuid.uuid4())

    def Init(self, tableName = 'Table', visionSensorName = 'Vision_sensor', binName = 'Bin', scaling = 0.004, visionSensorHeight = 1.93):
        self.bin = vo.VrepObject(self.vrepConn, binName)
        #self.bin.SetToDynamic() #commented out so that the bin cannot be moved during the simulation. #DGU - 20200922
        self.table = vo.VrepObject(self.vrepConn, tableName)
        self.visionSensor = vo.VrepObject(self.vrepConn, visionSensorName)
        self.shapeList = []
        self.scalingObj = scaling
        self.visionSensorHeight = visionSensorHeight
        self.visionSensor.SetObjectPosition([0.05, 0.125, visionSensorHeight])

    def Step(self):
        self.vrepConn.start()
        self.DrawMeshes()
        self.manipulator.RePaintElement(self.table, True)
        self.manipulator.RePaintElement(self.bin, True)
        time.sleep(1)  # so that every object falls down before pausing the simulation#DGU - 20200920
        self.vrepConn.pause()
        imgPath, deptPath, resolution = self.manipulator.GetImage(self.visionSensor.name)

        self.GetPropertiesOfScreenObjects(imgPath, deptPath, resolution)

        self.DeleteCreatedObjects()

    def GetPropertiesOfScreenObjects(self, path, deptBuffer, deptResolution):
        visionSensorPos = self.visionSensor.GetObjectPosition()
        visionSensorAngle = self.visionSensor.GetVisionSensorAngle(self.visionSensor.clientID, self.visionSensor.opMode)
        visionSensor = [visionSensorPos, visionSensorAngle]
        tablePos = self.table.GetObjectPosition()
        tableSize = self.table.GetObjectSize(self.table.clientID, self.table.opMode)
        table = [tablePos, tableSize]
        trainingImage = TI.TrainingImage(path, deptBuffer, deptResolution, self.guid, visionSensor, table)
        for element in self.shapeList:
            position_rel, orienatation_rel, size = element.GetObjectPositionAndOrientation(self.visionSensor.name)
            position_abs, orientation_abs, dummy_size = element.GetObjectPositionAndOrientation(None)
            trainingImage.addFixtureByParams(position_abs, orientation_abs, position_rel, orienatation_rel, size)

        self.mongoDb.insert(trainingImage.dictMapper())

    def DrawMeshes(self):
        for i in range(self.elementsCount):
            self.drawer.DrawMesh(self.meshName, self.scalingObj) #0.004->0.001
            if i == 0:
                self.AddShape("Shape")
            else: 
                self.AddShape("Shape"+str(i-1))

    def SetObjectsToDynamic(self, name, manipulator):
        success, objectIds = self.manipulator.GetObjects(name, self.elementsCount)
        if success is not -1:
            self.manipulator.SetObjectsToDynamic(name, objectIds)
        else:
            print('Error while get inserted object shapes from simulation.')

    def DeleteCreatedObjects(self):
        self.RemoveAllShapes()

    def AddShape(self, shapeName):
        self.shapeList.append(vo.VrepObject(self.vrepConn, shapeName))
        self.shapeList[-1].SetToDynamic()
    
    def RemoveShape(self, shape):
        self.shapeList.remove(shape)

    def RemoveAllShapes(self):
        for element in self.shapeList:
            element.Remove()
        self.shapeList = []
    
    def AddImportedMeshesToList(self, shapeNames):
        for element in shapeNames:
            self.shapeList.append(vo.VrepObject(self.vrepConn, element))