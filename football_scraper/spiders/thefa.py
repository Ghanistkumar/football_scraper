import scrapy, json, time
from football_scraper.helpers.scraper_handler import extract_league_id
from scrapy.loader import ItemLoader
from football_scraper.items import TheFaItem

class TheFaSpider(scrapy.Spider):
    name = 'thefa'
    
    # Starting URL (English football league system on Wikipedia)
    start_urls = ['https://fulltime.thefa.com/statLeaders/1/1000.html?selectedSeason=459314984&selectedFixtureGroupAgeGroup=0&selectedDivision=0&selectedStatisticDisplayMode=1']

    def parse(self, response):
        league_id = response.xpath('//*[@id="ft-header"]/nav[2]/div/ul/li[1]/a/@href').get()
        rows = response.xpath('//table/tbody/tr')

        for row in rows:
            thefaItems = ItemLoader(item=TheFaItem(), selector=row)

            # Adding data to the PlayerStatsItem fields
            thefaItems.add_xpath('position', './th[1]/text()')
            thefaItems.add_xpath('player_name', './th[2]')
            thefaItems.add_value('league_id', extract_league_id(league_id))
            thefaItems.add_xpath('player_id','./th[2]/a/@href')
            thefaItems.add_xpath('team', './th[3]/div/div[2]')
            thefaItems.add_xpath('appearances', './td[1]')
            thefaItems.add_xpath('overall_goals', './td[2]')
            thefaItems.add_xpath('goals', './td[3]')
            thefaItems.add_xpath('penalties', './td[4]')
            thefaItems.add_xpath('assists', './td[5]')
            thefaItems.add_xpath('yellow_cards', './td[6]')
            thefaItems.add_xpath('red_cards', './td[7]')
            thefaItems.add_xpath('second_yellow_card', './td[8]')
            thefaItems.add_xpath('sin_bin', './td[9]')
            thefaItems.add_xpath('started', './td[10]')
            thefaItems.add_xpath('subbed_on', './td[11]')
            thefaItems.add_xpath('subbed_off', './td[12]')
            thefaItems.add_xpath('bench_used', './td[13]')
            thefaItems.add_xpath('bench_unused', './td[14]')
            thefaItems.add_xpath('own_goal_conceded', './th[19]')
            thefaItems.add_xpath('captain', './th[20]')
            thefaItems.add_xpath('player_of_match', './th[21]')

            yield thefaItems.load_item()