from datetime import datetime as dtm
from football_scraper.config.db import PlayerTable
import json, pymongo
from bson import ObjectId

def storePlayers(footballPlayer):
    footballPlayer["created"] = dtm.utcnow()
    return PlayerTable.find_one_and_update({"player_wiki_id": footballPlayer['player_wiki_id']}, {"$set": footballPlayer}, upsert=True, new=True)

def getfootballPlayers(offset=0, limit=100, search=None):
    query = [
        {"$skip": int(offset)},
        {"$limit": int(limit)}
    ]
    
    if search != None:
        response = findfootballPlayer(f'"{search}"')
        count = len(response)
    else:
        result = list(PlayerTable.aggregate(query))
        for item in result:
            item['_id'] = str(item['_id'])
        response = json.loads(json.dumps(result, default=str))
        count = getfootballPlayersCount()

    return {
        "totalCount": count,
        "data": response,
    }

def getfootballPlayersCount():
    return PlayerTable.count_documents({})

def findfootballPlayer(text):
    index = [
        ("name", pymongo.TEXT),
        ("occupation", pymongo.TEXT),
        ("spouse", pymongo.TEXT),
        ("other_names", pymongo.TEXT),
        ("nationality", pymongo.TEXT),
        ("info", pymongo.TEXT)
    ]
    
    searchQuery = {
        "$text":{
            "$search": str(text).lower()
            }
    }
    
    PlayerTable.create_index(index)
    data = list(PlayerTable.find(searchQuery))
    return json.loads(json.dumps(data, default=str))

# def getfootballPlayersforSearch(offset=0, limit=100, isCirightPushed=False):

#     query = [
#         {
#             '$match':{"ciright_pushed": isCirightPushed}
#         },
#         {
#             "$project":{
                
#                 "_id":0,
#                 "id": {"$toString":"$_id"},
#                 "awards": "$awards",
#                 "birthDate": "$birth_date",
#                 "spouse": "$spouse",
#                 "children": "$children",
#                 "parent": "$parent",
#                 "education": "$education",
#                 "occupation": "$occupation",
#                 "honours": "$honours",
#                 "nationality": "$nationality",
#                 "citizenship": "$citizenship",
#                 "otherName": "$other_names",
#                 "deathDate": "$death_date",
#                 "info": "$info",
#                 "name": "$name",
#                 "wikiUrl": "$wiki_url"
#             }
#         },
#         {"$skip":offset},
#         {"$limit":limit}
#     ]

#     return list(footballPlayerTable.aggregate(query))

def updatefootballPlayerIds(data):
    for footballPlayer in data:
        updateData = {
            "updated": dtm.utcnow(),
            "manufactureId" : footballPlayer['value'],
            "company_pushed": True,
        }
        PlayerTable.find_one_and_update({"_id": ObjectId(footballPlayer["key"])}, {"$set": updateData})