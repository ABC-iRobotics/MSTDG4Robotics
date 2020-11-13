import DataEntities.Fixture as fx
import datetime
import collections

class TrainingImage:

    def __init__(self, imageUrl, deptUrl, resolution, trainingId, visionSensor, table, bin):
        self.imageUrl = imageUrl
        self.deptUrl = deptUrl
        self.resolution = resolution
        self.fixtures = []
        self.trainingId = trainingId
        self.visionSensor = visionSensor
        self.table = table
        self.bin = bin
        
    def addFixture(self, fixture):
        self.fixtures.append(fixture)
        
    def addFixtureByParams(self, abs_pos, abs_or, rel_pos, rel_or, size):
        fixture = fx.Fixture(abs_pos, abs_or, rel_pos, rel_or, size)
        self.addFixture(fixture)

    def dictMapper(self):
        return  {
                    'guid': self.trainingId,
                    'imageUrl': self.imageUrl, 
                    'deptUrl': self.deptUrl, 
                    'resolution': self.resolution,
                    'visionSensor':
                            {
                                'absolutePosition': self.visionSensor[0],
                                'perspectiveAngle': self.visionSensor[1]
                            },
                    'table':
                            {
                                'absolutePosition': self.table[0],
                                'size': self.table[1]
                            },
                    'bin':
                            {
                            'absolutePosition': self.bin[0],
                            'size': self.bin[1]
                            },
                    'fixtures': self.getFixturesDict()
                }
    
    def getFixturesDict(self):
        dictFixtures = []
        if len(self.fixtures) > 0:
            for i in self.fixtures:
                dictFixtures.append(i.dictMapper())
        return dictFixtures