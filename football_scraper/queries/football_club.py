from datetime import datetime as dtm
from football_scraper.config.db import ClubTable
import json, pymongo
from bson import ObjectId

def storeClubs(footballClub):
    footballClub["created"] = dtm.utcnow()
    return ClubTable.find_one_and_update({"club_wiki_id": footballClub['club_wiki_id']}, {"$set": footballClub}, upsert=True, new=True)

def getfootballClubs(offset=0, limit=100, search=None):
    query = [
        {"$skip": int(offset)},
        {"$limit": int(limit)}
    ]
    
    if search != None:
        response = findfootballClub(f'"{search}"')
        count = len(response)
    else:
        result = list(ClubTable.aggregate(query))
        for item in result:
            item['_id'] = str(item['_id'])
        response = json.loads(json.dumps(result, default=str))
        count = getfootballClubsCount()

    return {
        "totalCount": count,
        "data": response,
    }

def getfootballClubsCount():
    return ClubTable.count_documents({})

def findfootballClub(text):
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
    
    ClubTable.create_index(index)
    data = list(ClubTable.find(searchQuery))
    return json.loads(json.dumps(data, default=str))

# def getfootballClubsforSearch(offset=0, limit=100, isCirightPushed=False):

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

#     return list(footballClubTable.aggregate(query))

def updatefootballClubIds(data):
    for footballClub in data:
        updateData = {
            "updated": dtm.utcnow(),
            "manufactureId" : footballClub['value'],
            "company_pushed": True,
        }
        ClubTable.find_one_and_update({"_id": ObjectId(footballClub["key"])}, {"$set": updateData})