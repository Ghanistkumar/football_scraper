from datetime import datetime as dtm
from musicians.config.db import footballLeagueTable
import json, pymongo
from bson import ObjectId

def storefootballLeague(footballLeague):
    footballLeague["created"] = dtm.utcnow()
    return footballLeagueTable.find_one_and_update({"footballLeague_wiki_id": footballLeague['footballLeague_wiki_id']}, {"$set": footballLeague}, upsert=True, new=True)

def getfootballLeagues(offset=0, limit=100, search=None):
    query = [
        {"$skip": int(offset)},
        {"$limit": int(limit)}
    ]
    
    if search != None:
        response = findfootballLeague(f'"{search}"')
        count = len(response)
    else:
        result = list(footballLeagueTable.aggregate(query))
        for item in result:
            item['_id'] = str(item['_id'])
        response = json.loads(json.dumps(result, default=str))
        count = getfootballLeaguesCount()

    return {
        "totalCount": count,
        "data": response,
    }

def getfootballLeaguesCount():
    return footballLeagueTable.count_documents({})

def findfootballLeague(text):
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
    
    footballLeagueTable.create_index(index)
    data = list(footballLeagueTable.find(searchQuery))
    return json.loads(json.dumps(data, default=str))

# def getfootballLeaguesforSearch(offset=0, limit=100, isCirightPushed=False):

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

#     return list(footballLeagueTable.aggregate(query))

def updatefootballLeagueIds(data):
    for footballLeague in data:
        updateData = {
            "updated": dtm.utcnow(),
            "manufactureId" : footballLeague['value'],
            "ciright_pushed": True,
        }
        footballLeagueTable.find_one_and_update({"_id": ObjectId(footballLeague["key"])}, {"$set": updateData})