import scrapy, json, time
from football_scraper.helpers.scraper_handler import getAbsoluteUrl
from scrapy.loader import ItemLoader
from football_scraper.items import ClubsItem
class ClubsSpider(scrapy.Spider):
    name = 'clubs'
    
    # Starting URL (English football club system on Wikipedia)
    start_urls = ['https://en.wikipedia.org/wiki/English_football_club_system']

    def parse(self, response):

        """
        Parse the Wikipedia page to extract club names and URLs.
        """

        for row in response.xpath('//*[@class="wikitable"]/tbody/tr/td/p//a')[1:]:  # Skipping header row
            club_name = row.xpath('@title').get()
            club_url = row.xpath('@href').get()

            # Only proceed if both club_name and club_url are found and if the URL belongs to Wikipedia
            if club_name and club_url and club_url.startswith('/wiki/'):
                club_name = club_name.strip()
                full_club_url = response.urljoin(club_url)
                yield response.follow(full_club_url, self.parseClubData, meta={'club_url': full_club_url})

        # Save the extracted club data
        # with open('clubs.json', 'w') as f:
        #     json.dump(clubs, f, indent=4)


    def parseClubData(self, response):
        clubItems = ItemLoader(item=ClubsItem(), selector=response)
        clubItems.add_xpath('club_wiki_id', './/div[@class="club-id"]/text()')
        clubItems.add_xpath('title', './/h1[@class="club-title"]/text()')
        clubItems.add_xpath('description', './/div[@class="club-description"]')
        clubItems.add_xpath('inception_date', './/span[@class="inception-date"]/text()')
        clubItems.add_xpath('mobile', './/span[@class="mobile"]/text()')
        clubItems.add_xpath('insta_profile', './/a[@class="insta-profile"]/@href')
        clubItems.add_xpath('linkedin_profile', './/a[@class="linkedin-profile"]/@href')
        clubItems.add_xpath('twitter_profile', './/a[@class="twitter-profile"]/@href')
        clubItems.add_xpath('website_url', './/a[@class="website"]/@href')
        clubItems.add_xpath('post_code', './/span[@class="post-code"]/text()')
        clubItems.add_xpath('address', './/span[@class="address"]/text()')
        clubItems.add_xpath('country', './/span[@class="country"]/text()')
        clubItems.add_xpath('state', './/span[@class="state"]/text()')
        clubItems.add_xpath('city', './/span[@class="city"]/text()')
        clubItems.add_xpath('zipcode', './/span[@class="zipcode"]/text()')
        clubItems.add_xpath('logo', './/img[@class="club-logo"]/@src')

        yield clubItems.load_item()