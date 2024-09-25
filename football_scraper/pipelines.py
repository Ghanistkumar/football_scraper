# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class FootballScraperPipeline:

    def __init__(self):
        print("Initialized mongodb pipline")

    def process_item(self, item, spider):
        if spider.name == "football":
            footballDict = ItemAdapter(item).asdict()
            football = storeFootball(footballDict)
            return football
