from football_scraper.helpers.scraper_handler import printError, printSuccess, printInfo
from datetime import datetime as dtm
import requests, json, sys
from football_scraper.queries.football_thefa import getAllData
from football_scraper.config.config import COMPANY_ENDPOINT_BASE_URL

# def addFootballDataToServer(offset=0, limit=500, target_type="Person"):

#     print(f"Starting to send football data to COMPANY server {dtm.now()}")
#     sys.stdout.flush()
#     artist = getfootballLeagues(offset, limit, target_type)

#     if artist and len(artist) > 0:
#         payload = {
#                 "player_stat": json.loads(json.dumps(artist, default=str))
#             }
#         res = requests.post(
#                 COMPANY_ENDPOINT_BASE_URL + "", 
#                 json=payload
#             ).json()
            
#         #handling the response from COMPANY and updating the data with manufacture Id
#         if res['status'] and res['message'] == 'success':
#             printSuccess(f"Artist data added successfully to COMPANY Server at {dtm.now()} with offset={offset} and limit={limit}")
#             sys.stdout.flush()
#             printSuccess(f"Returned success response from COMPANY: {res}")
#             sys.stdout.flush()
#             updatefootballLeagueIds(res["data"])

#             printInfo(f"Running another batch for artist data..")
#             sys.stdout.flush()  
#             addFootballDataToServer()
#         else:
#             printError(f"Failed to send artist data to COMPANY Server. Attempted at {dtm.now()}")
#             sys.stdout.flush()
#             printError(f"Returned failed response from COMPANY: {res}")
#             sys.stdout.flush()
#             printInfo(f"Failed Payload: {payload}")
#             sys.stdout.flush()
#             return
#     else:
#         printInfo(f"No league data returned from databases, ABORTING COMPANY Push. Attempted at {dtm.now()}")
#         sys.stdout.flush()
#         return

def addFootballDataToServer(league_id, season_id):
    print(f"Starting to send football data to COMPANY server {dtm.now()}")
    sys.stdout.flush()
    # scraped_data = getAllData()

    with open('all_items.json', "r") as f:
        scraped_data = json.load(f)
    if scraped_data and len(scraped_data) > 0:

        payload = {
            "league_id": str(league_id),
            "season_id": str(season_id),
            "player_statistics": json.loads(json.dumps(scraped_data, default=str))
        }
        print(payload)
        
        try:
            headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
            }
            response = requests.post(COMPANY_ENDPOINT_BASE_URL, data=json.dumps(payload), headers=headers)
            print(f"Raw response: {response.json()}")
            
            res = response.json()
            if(res["status"]):
                return printInfo(f"Data successfully sent to Company. Attempted at {dtm.now()}")
            else:
                return printInfo(f"Data Not sent to Company. Attempted at {dtm.now()}")
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        # except json.JSONDecodeError as e:
        #     print(f"Error decoding JSON response: {e}")
        #     print(f"Raw response: {response.text}")
    else:
        printInfo(f"No league data returned from databases, ABORTING COMPANY Push. Attempted at {dtm.now()}")
        sys.stdout.flush()
        return
