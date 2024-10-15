# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from football_scraper.queries.football_league import storeLeagues
from football_scraper.queries.football_club import storeClubs
from football_scraper.queries.football_player import storePlayers

class FootballScraperPipeline:

    def __init__(self):
        print("Initialized mongodb pipline")

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
            return leagues
        if spider.name == "players":
            playersDict = ItemAdapter(item).asdict()
            players = storePlayers(playersDict)
            print(players)
            return leagues
