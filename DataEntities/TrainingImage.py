import DataEntities.Fixture as fx
import datetime

class TrainingImage:

    def __init__(self, imageUrl, deptBuffer, deptResolution):
        self.imageUrl = imageUrl
        self.deptBuffer = deptBuffer
        self.deptResolution = deptResolution
        self.fixtures = []
        
    def addFixture(self, fixture):
        self.fixtures.append(fixture)
        
    def addFixtureByParams(self, abs_pos, abs_or, rel_pos, rel_or):
        fixture = fx.Fixture(abs_pos, abs_or, rel_pos, rel_or)
        self.addFixture(fixture)

    def dictMapper(self):
        return  {
                    'imageUrl': self.imageUrl, 
                    'deptBuffer': self.deptBuffer, 
                    'deptResolution': self.deptResolution, 
                    'fixtures': self.getFixturesDict()
                }
    
    def getFixturesDict(self):
        dictFixtures = []
        if len(self.fixtures) > 0:
            for i in self.fixtures:
                dictFixtures.append(i.dictMapper())
        return dictFixtures