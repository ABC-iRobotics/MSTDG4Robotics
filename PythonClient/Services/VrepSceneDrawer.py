import sys, os, glob
import Helper as hp

class VrepSceneDrawer:
    
    def __init__(self, vrepConn, binPickingScene, functionName='insertMesh', folderName = 'meshes/' ):
        self.functionName = functionName
        self.vrepConn = vrepConn
        self.folderName = folderName    
        self.binPickingScene = binPickingScene
        self.helper = hp.Helper()

    def GetMeshList(self):
        globalPath = os.path.dirname(__file__)
        if self.meshName is not None:
            fileNames = glob.glob( globalPath +'/../' +self.folderName + self.meshName)
        else:    
            fileNames = glob.glob( globalPath +'/../' +self.folderName + "*.stl")
        return fileNames

    def DrawMesh(self, meshName, scaling):
        self.meshName = meshName
        meshList = self.GetMeshList()
        floatParamList = self.helper.GetColors(True)
        scale = scaling
        floatParamList.append(scale)
        floatParamList.extend(self.helper.GetAbsolutePosition(True))
        floatParamList.extend(self.helper.GetAbsoluteOrientation(True))

        separator = ',\n'
        print('Call '+self.functionName+ ' with '+ separator.join(meshList)+' parameter.')
        ret, ints, floats, strings, buffs = self.vrepConn.callScript(self.functionName, inStrings=meshList, inFloats=floatParamList)
        return ret, ints, floats, strings, buffs
        
