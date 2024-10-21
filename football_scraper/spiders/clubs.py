import scrapy, json, time
from football_scraper.config.config import locations
from football_scraper.helpers.scraper_handler import getAbsoluteUrl
from scrapy.loader import ItemLoader
from football_scraper.items import ClubsItem
from scrapy import Request

class ClubsSpider(scrapy.Spider):
    name = 'clubs'
    
    def start_requests(self):
        baseUrls = locations.leagues_url
        for reqUrl in baseUrls:
            yield Request(url=reqUrl, callback=self.parse, meta={'dont_redirect': True})


    def parse(self, response):
        listingUrls = []
        table_head_xpath = '//table[@class="wikitable"]/tbody/tr[th/text()="Club\n"]'
        if(response.xpath(table_head_xpath)) is not None:
            for item in response.xpath('//table[@class="wikitable"]/tbody/tr/td[1]/a'):
                listing_url = getAbsoluteUrl(response.request.url, item.xpath('@href').get())
                if listing_url:
                    listingUrls.append(listing_url) 
            
            # print(listingUrls)
            if listingUrls:
                for url in listingUrls:
                    yield Request(url, self.parseClubData, meta={'club_url': url})
                    time.sleep(3)


    def parseClubData(self, response):
        clubItems = ItemLoader(item=ClubsItem(), selector=response)
        clubItems.add_xpath('club_wiki_id', '//*[@id="t-wikibase"]/a/@href')
        clubItems.add_xpath('title', '//tr[th/text()="Full name"]/td')
        clubItems.add_xpath('nickname', '//tr[th/text()="Nickname(s)"]/td')
        clubItems.add_xpath('description', '//*[@id="mw-content-text"]/div[1]/p[2]')
        clubItems.add_xpath('inception_date', '//tr[th/text()="Founded"]/td')
        clubItems.add_xpath('chairman', '//tr[th/text()="Chairman"]/td')
        clubItems.add_xpath('manager', '//tr[th/text()="Manager"]/td')
        clubItems.add_xpath('league', '//tr[th/text()="League"]/td')
        clubItems.add_xpath('ground', '//tr[th/text()="Ground"]/td')
        # clubItems.add_xpath('mobile', './/span[@class="mobile"]/text()')
        # clubItems.add_xpath('insta_profile', './/a[@class="insta-profile"]/@href')
        # clubItems.add_xpath('linkedin_profile', './/a[@class="linkedin-profile"]/@href')
        # clubItems.add_xpath('twitter_profile', './/a[@class="twitter-profile"]/@href')
        clubItems.add_value('website_url', response.xpath('//ul/li/a[contains(@class, "external text")]/@href').get())
        # clubItems.add_xpath('post_code', './/span[@class="post-code"]/text()')
        # clubItems.add_xpath('address', './/span[@class="address"]/text()')
        clubItems.add_xpath('country', '//tr[th/text()="Country"]/td')
        # clubItems.add_xpath('state', './/span[@class="state"]/text()')
        # clubItems.add_xpath('city', './/span[@class="city"]/text()')
        # clubItems.add_xpath('zipcode', './/span[@class="zipcode"]/text()')
        clubItems.add_value('logo', 'https:' + response.xpath('//img[@class="mw-file-element"]/@src[1]').get())

        yield clubItems.load_item()