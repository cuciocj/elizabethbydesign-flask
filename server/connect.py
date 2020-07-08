from pymongo import MongoClient

class Connect(object):
    @staticmethod
    def get_connection():
        return MongoClient("mongodb://127.0.0.1:27017/Elizabeth_DB")