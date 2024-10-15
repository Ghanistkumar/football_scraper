import scrapy, json, time
from football_scraper.helpers.scraper_handler import getAbsoluteUrl
from scrapy.loader import ItemLoader
from football_scraper.items import LeaguesItem

class LeaguesSpider(scrapy.Spider):
    name = 'leagues'
    
    # Starting URL (English football league system on Wikipedia)
    start_urls = ['https://en.wikipedia.org/wiki/English_football_league_system']

    def parse(self, response):

        """
        Parse the Wikipedia page to extract league names and URLs.
        """

        for row in response.xpath('//*[@class="wikitable"]/tbody/tr/td/p//a')[1:]:  # Skipping header row
            league_name = row.xpath('@title').get()
            league_url = row.xpath('@href').get()

            # Only proceed if both league_name and league_url are found and if the URL belongs to Wikipedia
            if league_name and league_url and league_url.startswith('/wiki/'):
                league_name = league_name.strip()
                full_league_url = response.urljoin(league_url)
                yield response.follow(full_league_url, self.parseLeagueData, meta={'league_url': full_league_url})

        # Save the extracted league data
        # with open('leagues.json', 'w') as f:
        #     json.dump(leagues, f, indent=4)


    def parseLeagueData(self, response):
        leagueItems = ItemLoader(item=LeaguesItem(), selector=response)
        leagueItems.add_xpath('league_wiki_id', '//*[@id="t-wikibase"]/a/@href')
        leagueItems.add_value('league_url', response.meta['league_url'])
        leagueItems.add_xpath('title', '//*[@id="mw-content-text"]/div[1]/table[1]/caption')
        leagueItems.add_value('logo', 'https:' + response.xpath( '//td[@class="infobox-image"]/span/a/img/@src').get())
        leagueItems.add_value('country', 'United Kingdom')
        leagueItems.add_xpath('region', '//tr[th/text()="Country"]/td')
        leagueItems.add_xpath('no_of_teams', '//tr[th/text()="Number of teams"]/td')
        leagueItems.add_xpath('current_champions', '//tr[th/text()="Current champions"]/td')
        # leagueItems.add_xpath('season_list', '')

        yield leagueItems.load_item()