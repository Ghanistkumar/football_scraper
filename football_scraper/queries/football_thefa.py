from datetime import datetime as dtm
from football_scraper.config.db import TheFaTable
from bson import ObjectId

def storeTheFa(theFa):
    theFa["created"] = dtm.utcnow()
    return TheFaTable.find_one_and_update({"player_id": theFa['player_id']}, {"$set": theFa}, upsert=True, new=True)

def storeSingleRecord(theFa):
    theFa["created"] = dtm.utcnow()
    return TheFaTable.insert_one(theFa)

def gettheFasCount():
    return TheFaTable.count_documents({})

def getAllData():
    return list(TheFaTable.find({}, {"_id": 0}))
