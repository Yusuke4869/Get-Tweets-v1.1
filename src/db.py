import os
import dns.resolver
import pymongo
import certifi

DB_URI = os.environ["DB_URI"]
client = pymongo.MongoClient(DB_URI, tlsCAFile=certifi.where())

class DataBase:

    def __init__(self, database_name, collection_name) -> None:
        self.db = client[database_name]
        self.collection = self.db[collection_name]

    def update_one(self, filter: dict, update_data: dict) -> None:
        if not self.find_one(filter):
            self.collection.insert_one(update_data)
        else:
            self.collection.update_one(filter, {"$set":update_data})

    def find_one(self, filter: dict) -> dict:
        return self.collection.find_one(filter)