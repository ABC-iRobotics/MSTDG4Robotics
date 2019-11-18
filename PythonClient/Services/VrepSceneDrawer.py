import sys, os, glob
import Helper as hp

class VrepSceneDrawer:
    
    def __init__(self, vrepConn, taskName='BinPicking', functionName='insertMesh', folderName = 'meshes/'):
        self.functionName = functionName
        self.vrepConn = vrepConn
        self.folderName = folderName    
        self.helper = hp.Helper()
        self.taskName = taskName

    def GetMeshList(self):
        globalPath = os.path.dirname(__file__)
        if self.meshName is not None:
            fileName = glob.glob( globalPath +'/../' +self.folderName+'/'+self.taskName+'/'+ self.meshName)
        else:    
            fileName = glob.glob( globalPath +'/../' +self.folderName + "*.stl")
        return fileName

    def DrawMesh(self, meshName, scaling = 1, colors = None, position = None, orientation = None):
        self.meshName = meshName
        meshList = self.GetMeshList()
        floatParamList = []
        if colors is None:
            floatParamList = self.helper.GetColors(True)
        else:
            floatParamList = colors
        
        scale = scaling
        
        floatParamList.append(scale)
        
        if position is None:
            floatParamList.extend(self.helper.GetRandomAbsolutePosition(True))
        else: 
            floatParamList.extend(position)
        if orientation is None:
            floatParamList.extend(self.helper.GetRandomAbsoluteOrientation(True))
        else:
            floatParamList.extend(orientation)

        separator = ',\n'
        print('Call '+self.functionName+ ' with '+ separator.join(meshList)+' parameter.')
        ret, ints, floats, strings, buffs = self.vrepConn.callScript(self.functionName, inStrings=meshList, inFloats=floatParamList)
        return ret, ints, floats, strings, buffs
        
