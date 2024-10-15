import scrapy, json, time
from football_scraper.helpers.scraper_handler import getAbsoluteUrl
from scrapy.loader import ItemLoader
from football_scraper.items import PlayersItem
class PlayersSpider(scrapy.Spider):
    name = 'players'
    
    # Starting URL (English football player system on Wikipedia)
    start_urls = ['https://en.wikipedia.org/wiki/English_football_player_system']

    def parse(self, response):

        """
        Parse the Wikipedia page to extract player names and URLs.
        """

        for row in response.xpath('//*[@class="wikitable"]/tbody/tr/td/p//a')[1:]:  # Skipping header row
            player_name = row.xpath('@title').get()
            player_url = row.xpath('@href').get()

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
        playerItems.add_xpath('player_wiki_id', './/div[@class="player-id"]/text()')
        playerItems.add_xpath('first_name', './/span[@class="first-name"]/text()')
        playerItems.add_xpath('last_name', './/span[@class="last-name"]/text()')
        playerItems.add_xpath('date_of_birth', './/span[@class="dob"]/text()')
        playerItems.add_xpath('gender', './/span[@class="gender"]/text()')
        playerItems.add_xpath('country_dialling_code', './/span[@class="dial-code"]/text()')
        playerItems.add_xpath('country_code_alpha', './/span[@class="country-code-alpha"]/text()')
        playerItems.add_xpath('mobile', './/span[@class="mobile"]/text()')
        playerItems.add_xpath('height', './/span[@class="height"]/text()')
        playerItems.add_xpath('weight', './/span[@class="weight"]/text()')
        playerItems.add_xpath('dominant_foot', './/span[@class="dominant-foot"]/text()')
        playerItems.add_xpath('position', './/span[@class="position"]/text()')
        playerItems.add_xpath('current_club', './/span[@class="current-club"]/text()')
        playerItems.add_xpath('logo', './/img[@class="player-logo"]/@src')
        playerItems.add_xpath('description', './/div[@class="player-description"]')  # HTML, remove_tags will process it
        playerItems.add_xpath('insta_profile', './/a[@class="insta-profile"]/@href')
        playerItems.add_xpath('linkedin_profile', './/a[@class="linkedin-profile"]/@href')
        playerItems.add_xpath('twitter_profile', './/a[@class="twitter-profile"]/@href')
        playerItems.add_xpath('website_url', './/a[@class="website"]/@href')
        playerItems.add_xpath('post_code', './/span[@class="post-code"]/text()')
        playerItems.add_xpath('address', './/span[@class="address"]/text()')
        playerItems.add_xpath('country', './/span[@class="country"]/text()')
        playerItems.add_xpath('state', './/span[@class="state"]/text()')
        playerItems.add_xpath('city', './/span[@class="city"]/text()')
        playerItems.add_xpath('zipcode', './/span[@class="zipcode"]/text()')

        yield playerItems.load_item()