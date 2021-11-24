import os
import pymongo


class Database(object):
    URI = os.environ.get("MONGODB_URI")
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['resapp']

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
    def update_one(collection, filtered, query):
        return Database.DATABASE[collection].update_one(filtered, query)

    @staticmethod
    def update_one_filter(collection, filtered, query, array_filters, upsert=None):
        return Database.DATABASE[collection].update_one(filtered, query, array_filters, upsert)

    @staticmethod
    def update_many(collection, filtered, query):
        return Database.DATABASE[collection].update_many(filtered, query)

    @staticmethod
    def delete_one(collection, filtered):
        return Database.DATABASE[collection].delete_one(filtered)

    @staticmethod
    def delete_many(collection, filtered, query):
        return Database.DATABASE[collection].delete_many(filtered, query)
