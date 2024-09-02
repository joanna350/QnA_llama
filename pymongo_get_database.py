from pymongo import MongoClient


def get_database():

    CONNECTION_STRING = "mongodb://localhost:27017"

    client = MongoClient(CONNECTION_STRING)

    db = client.get_database('test')

    return db


if __name__ == '__main__':
    get_database()