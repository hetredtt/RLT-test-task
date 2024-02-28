import pymongo
from pymongo.errors import ConnectionFailure, PyMongoError

class MongoDBConnection:
    def __init__(self, host='localhost', port=27017, db_name='mydatabase'):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = pymongo.MongoClient(self.host, self.port)
            if self.db_name:
                self.db = self.client[self.db_name]
            return True
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            return False

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
            self.db = None


    def find_documents(self, collection_name, query):
        if self.db is not None:
            collection = self.db[collection_name]
            try:
                cursor = collection.aggregate(query)
                return list(cursor)
            except PyMongoError as e:
                print(f"Failed to find documents: {e}")
                return []
        else:
            print("Not connected to a database.")