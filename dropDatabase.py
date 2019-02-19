from pymongo import MongoClient

clientMongo = MongoClient()
clientMongo.drop_database("savia")
clientMongo.drop_database("postsavia")
