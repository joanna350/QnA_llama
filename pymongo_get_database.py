from pymongo import MongoClient
import pymongo

import motor.motor_asyncio


def get_database():
    """
    receive in string the database name to retrieve data from
    :param name: give the name of the database
    :return: the database with the name
    """

    CONNECTION_STRING = "mongodb://localhost:27017"

    client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING)

    db = client.test_database
    print('db connection=================')
    print(db)
    return db


if __name__ == '__main__':

    get_database()

    # client = pymongo.MongoClient("localhost", 27017, maxPoolSize=50)
    #
    # d = dict((db, [collection for collection in client[db].list_collection_names()])
    #          for db in client.list_database_names())
    # print(d)