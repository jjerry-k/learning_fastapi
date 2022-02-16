import pymongo
import datetime

def connect():
    host = "0.0.0.0"
    port = "27017"
    db = "test"
    coll = "ex"

    conn = pymongo.MongoClient(f"mongodb://{host}:{port}")

    today = datetime.datetime.now().date()
    conn[db][coll].insert_one(
        {
        "name":"Test",
        "today": str(today)
    }
    )

    docs = conn[db][coll].find()
    for doc in docs:
        print(doc)

connect()