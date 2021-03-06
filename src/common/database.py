import pymongo
import os

class Database(object):
    URI = os.environ.get("MONGODB_URI")
    DATABASE = None

    @staticmethod
    def initialize():
        connection = pymongo.MongoClient(Database.URI, int(os.environ.get("MONGODB_PORT")))
        Database.DATABASE = connection[os.environ.get("MONGODB_NAME")]
        #Database.DATABASE.authenticate(os.environ.get("MONGODB_USER"), os.environ.get("MONGODB_PASS"))


    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)