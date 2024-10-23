import scrapy, json, time
from football_scraper.helpers.scraper_handler import getAbsoluteUrl
from football_scraper.config.config import locations
from scrapy.loader import ItemLoader
from football_scraper.items import PlayersItem
from scrapy import Request

class PlayersSpider(scrapy.Spider):
    name = 'players'
    
    start_urls = ['https://en.wikipedia.org/wiki/List_of_football_clubs_in_England']
    # Starting URL (English football player system on Wikipedia)
    def parse(self, response):

        """
        Parse the Wikipedia page to extract league names and URLs.
        """

        for row in response.xpath('//*[@id="mw-content-text"]/div[1]/table/tbody/tr/td[1]/a'):  # Skipping header row
            club = row.xpath('@title').get()
            club_url = row.xpath('@href').get()

            # Only proceed if both club and club_url are found and if the URL belongs to Wikipedia
            # if club and club_url and club_url.startswith('/wiki/'):
            #     club = club.strip()
            full_club_url = response.urljoin(club_url)
            yield Request(full_club_url, self.parsePlayers, meta={'club_url': full_club_url})

    def parsePlayers(self, response):

        """
        Parse the Wikipedia page to extract player names and URLs.
        """
        player_tbl_xpath = "//table[contains(@class,'football-squad')]/tbody/tr/td[4]//a"
        if(response.xpath(player_tbl_xpath)):
            for row in response.xpath('//table[contains(@class,"football-squad")]/tbody/tr/td[4]//a'):
                player_name = row.xpath('@title').get()
                player_url = row.xpath('@href').get()
                print(player_url)
                # Only proceed if both player_name and player_url are found and if the URL belongs to Wikipedia
                if player_name and player_url and player_url.startswith('/wiki/'):
                    player_name = player_name.strip()
                    full_player_url = response.urljoin(player_url)
                    yield response.follow(full_player_url, self.parsePlayerData, meta={'player_url': full_player_url})

        # Save the extracted player data
        # with open('players.json', 'w') as f:
        #     json.dump(players, f, indent=4)


    def parsePlayerData(self, response):
        playerItems = ItemLoader(item=PlayersItem(), selector=response)
        playerItems.add_xpath('player_wiki_id', '//*[@id="t-wikibase"]/a/@href')
        playerItems.add_value('wiki_url', response.meta['player_url'])
        #need to split first name and last name
        playerItems.add_xpath('first_name', '//caption[contains(@class, "infobox-title")]')
        playerItems.add_xpath('last_name', '//caption[contains(@class, "infobox-title")]')
        playerItems.add_xpath('date_of_birth', '//tr[th/text()="Date of birth"]/td')
        playerItems.add_xpath('gender', './/span[@class="gender"]/text()')
        #layerItems.add_xpath('country_dialling_code', './/span[@class="dial-code"]/text()')
        #playerItems.add_xpath('country_code_alpha', './/span[@class="country-code-alpha"]/text()')
        playerItems.add_value('player_image', 'https:' + response.xpath('//img[@class="mw-file-element"]/@src[1]').get())
        playerItems.add_xpath('height', '//tr[th/text()="Height"]/td')
        playerItems.add_xpath('weight', './/span[@class="weight"]/text()')
        #playerItems.add_xpath('dominant_foot', './/span[@class="dominant-foot"]/text()')
        playerItems.add_xpath('position', '//tr[th/text()="Position(s)"]/td')
        playerItems.add_xpath('current_club', '//tr[th//text()="Current team"]/td')
        #playerItems.add_xpath('logo', './/img[@class="player-logo"]/@src')
        playerItems.add_xpath('description', '//*[@id="mw-content-text"]/div[1]/p[2]')  # HTML, remove_tags will process it
        # playerItems.add_xpath('insta_profile', './/a[@class="insta-profile"]/@href')
        # playerItems.add_xpath('linkedin_profile', './/a[@class="linkedin-profile"]/@href')
        # playerItems.add_xpath('twitter_profile', './/a[@class="twitter-profile"]/@href')
        # playerItems.add_xpath('website_url', './/a[@class="website"]/@href')
        # playerItems.add_xpath('post_code', './/span[@class="post-code"]/text()')
        # playerItems.add_xpath('address', './/span[@class="address"]/text()')
        #need to split by , and get [1] as country
        playerItems.add_xpath('country', '//tr[th/text()="Position(s)"]/td')
        playerItems.add_xpath('state', './/span[@class="state"]/text()')
        playerItems.add_xpath('city', './/span[@class="city"]/text()')
        playerItems.add_xpath('zipcode', './/span[@class="zipcode"]/text()')

        yield playerItems.load_item()