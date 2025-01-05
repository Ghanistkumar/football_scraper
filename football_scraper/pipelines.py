# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from football_scraper.queries.football_league import storeLeagues
from football_scraper.queries.football_club import storeClubs
from football_scraper.queries.football_player import storePlayers
from football_scraper.queries.football_thefa import storeSingleRecord
import json
class FootballScraperPipeline:

    def __init__(self):
        self.all_items = []
        print("Initialized mongodb pipline")
    
    def close_spider(self, spider):
    # Save all items to a JSON file
        with open("all_items.json", "w") as f:
            json.dump(self.all_items, f, indent=4)

    def process_item(self, item, spider):
        if spider.name == "leagues":
            leaguesDict = ItemAdapter(item).asdict()
            leagues = storeLeagues(leaguesDict)
            print(leaguesDict)
            return leagues
        if spider.name == "clubs":
            clubsDict = ItemAdapter(item).asdict()
            clubs = storeClubs(clubsDict)
            print(clubs)
            return clubs
        if spider.name == "players":
            playersDict = ItemAdapter(item).asdict()
            players = storePlayers(playersDict)
            print(players)
            return players
        
        if spider.name == "thefa":
            theFasDict = ItemAdapter(item).asdict()
            # players = storeSingleRecord(theFasDict)
            # print(theFasDict)
            self.all_items.append(theFasDict)
            return theFasDict
