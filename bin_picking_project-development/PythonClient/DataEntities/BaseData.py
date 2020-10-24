import DataEntities.Fixture as fx
import datetime

class BaseData:

    def __init__(self, trainingId):
        self.fixtures = []
        self.trainingId = trainingId
        
    def addFixture(self, fixture):
        self.fixtures.append(fixture)
        
    def addFixtureByParams(self, abs_pos, abs_or, rel_pos, rel_or):
        fixture = fx.Fixture(abs_pos, abs_or, rel_pos, rel_or)
        self.addFixture(fixture)

    def dictMapper(self, name):
        return  {
                    'guid': self.trainingId,
                    name: self.getFixturesDict()
                }
    
    def getFixturesDict(self):
        dictFixtures = []
        if len(self.fixtures) > 0:
            for i in self.fixtures:
                dictFixtures.append(i.dictMapper())
        return dictFixtures