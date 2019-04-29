import pymongo as dbconn

class MongoService:
    def __init__(self, serverUri = 'localhost:27017/', databaseName = 'binPicking', collectionName='TrainingImage'):
      
        self.myclient = dbconn.MongoClient('mongodb://'+serverUri)
        dblist = self.myclient.list_database_names()
        if databaseName in dblist:
            print("MongoService: The database exists: "+ databaseName)
        else:
            print("MongoService: New database created successfully: "+databaseName)
        
        self.mydb = self.myclient[databaseName]

        self.createCollection(collectionName)

    def createCollection(self, collectionName):
        collist = self.mydb.list_collection_names()
        if collectionName in collist:
            print("MongoService: The collection exists: "+collectionName + " Scope changed.")
        else:
            print("MongoService: New collection created successfully: "+collectionName)
        self.mycol = self.mydb[collectionName]

    def insert(self, entity):
        element = self.mycol.insert_one(entity)
        print('MongoService: Entity inserted ' + str(element.inserted_id))
        return element.inserted_id
    
    def find(self, query ={}, includeExclude ={}):
        lastFindDoc = self.mycol.find(query, includeExclude)
        return lastFindDoc

    def update(self, query, newEntity):
        entity = self.mycol.find(query)
        self.mycol.update_one(query, newEntity)
        print('MongoService: Entity updated ' + entity.inserted_id)
    
    def delete(self, query):
        entity = self.mycol.find(query)
        self.mycol.delete_one(query)
        print('MongoService: Entity deleted ' + entity.inserted_id)
