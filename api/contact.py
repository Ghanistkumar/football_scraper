from football_scraper.helpers.scraper_handler import printError, printSuccess, printInfo
from datetime import datetime as dtm
import requests, json, sys
from football_scraper.queries.football_league import getfootballLeagues, updatefootballLeagueIds
from football_scraper.config.config import COMPANY_ENDPOINT_BASE_URL

def addFootballDataToServer(offset=0, limit=500, target_type="Person"):

    print(f"Starting to send football data to COMPANY server {dtm.now()}")
    sys.stdout.flush()
    artist = getfootballLeagues(offset, limit, target_type)

    if artist and len(artist) > 0:
        payload = {
                "football": json.loads(json.dumps(artist, default=str))
            }
        res = requests.post(
                COMPANY_ENDPOINT_BASE_URL + "", 
                json=payload
            ).json()
            
        #handling the response from COMPANY and updating the data with manufacture Id
        if res['status'] and res['message'] == 'success':
            printSuccess(f"Artist data added successfully to COMPANY Server at {dtm.now()} with offset={offset} and limit={limit}")
            sys.stdout.flush()
            printSuccess(f"Returned success response from COMPANY: {res}")
            sys.stdout.flush()
            updatefootballLeagueIds(res["data"])

            printInfo(f"Running another batch for artist data..")
            sys.stdout.flush()  
            addFootballDataToServer()
        else:
            printError(f"Failed to send artist data to COMPANY Server. Attempted at {dtm.now()}")
            sys.stdout.flush()
            printError(f"Returned failed response from COMPANY: {res}")
            sys.stdout.flush()
            printInfo(f"Failed Payload: {payload}")
            sys.stdout.flush()
            return
    else:
        printInfo(f"No league data returned from databases, ABORTING COMPANY Push. Attempted at {dtm.now()}")
        sys.stdout.flush()
        return
