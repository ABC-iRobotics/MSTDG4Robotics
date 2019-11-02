import Services.VrepObject as vo
import Services.VrepMeshDrawer as vdrawer
import Services.VrepSceneManipulator as sceneMan

import DataEntities.TrainingImage as TI
import DataEntities.Fixture as F
import Services.MongoScv as MS 

class BinPickingScene:
    def __init__(self, vrepConnector, tableName, binName, visionSensorName, elementsCount = 10, dbRowToAddCount = 10):
        self.elementsCount = elementsCount
        self.dbRowToAddCount = dbRowToAddCount

        self.vrepConn = vrepConnector

        self.drawer = vdrawer.VrepMeshDrawer(vrepConnector, self)
        self.manipulator = sceneMan.VrepSceneManipulator(vrepConnector, self)
        self.mongoDb = MS.MongoService()

        self.bin = vo.VrepObject(vrepConnector, binName)
        self.bin.SetToDynamic()

        self.table = vo.VrepObject(vrepConnector, tableName)
        self.visionSencor = vo.VrepObject(vrepConnector, visionSensorName)
        self.shapeList = []

    def StartLoop(self):
        for i in range(self.dbRowToAddCount):
            self.DrawMeshes()

            #self.SetObjectsToDynamic('Shape', self.manipulator)
            

            self.manipulator.RePaintElement(self.table, True)
            self.manipulator.RePaintElement(self.bin, True)

            imgPath, deptPath, resolution = self.manipulator.GetImage('Vision_sensor')
            
            self.GetPropertiesOfScreenObjects(imgPath, deptPath, resolution)

            self.DeleteCreatedObjects()

    def GetPropertiesOfScreenObjects(self, path, deptBuffer, deptResolution):
        trainingImage = TI.TrainingImage(path, deptBuffer, deptResolution)

        for element in self.shapeList:
            position_rel, orienatation_rel = element.GetObjectPositionAndOrientation('Vision_sensor')
            position_abs, orientation_abs = element.GetObjectPositionAndOrientation(None)
            trainingImage.addFixtureByParams(position_abs, orientation_abs, position_rel, orienatation_rel)

        self.mongoDb.insert(trainingImage.dictMapper())

    def DrawMeshes(self):
        for i in range(self.elementsCount):
            self.drawer.DrawMesh()
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