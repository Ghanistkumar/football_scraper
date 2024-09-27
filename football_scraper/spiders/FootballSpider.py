import scrapy, json, time
from football_scraper.helpers.scraper_handler import getAbsoluteUrl

class FootballSpider(scrapy.Spider):
    name = 'football'
    
    # Starting URL (English football league system on Wikipedia)
    start_urls = ['https://en.wikipedia.org/wiki/English_football_league_system']

    def parse(self, response):

        """
        Parse the Wikipedia page to extract league names and URLs.
        """
        leagues = []
        for row in response.xpath('//*[@class="wikitable"]/tbody/tr/td/p/b/a')[1:]:  # Skipping header row
            league_name = row.xpath('@title').get()
            league_url = row.xpath('@href').get()
        for row in response.xpath('//*[@class="wikitable"]/tbody/tr/td/p/b/a')[1:]:  # Skipping header row
            league_name = row.xpath('@title').get()
            league_url = row.xpath('@href').get()

            # Only proceed if both league_name and league_url are found and if the URL belongs to Wikipedia
            if league_name and league_url and league_url.startswith('/wiki/'):
            # Only proceed if both league_name and league_url are found and if the URL belongs to Wikipedia
            if league_name and league_url and league_url.startswith('/wiki/'):
                league_name = league_name.strip()
                full_league_url = response.urljoin(league_url)
                leagues.append({
                    'league_name': league_name,
                    'league_url': full_league_url
                })
                yield response.follow(full_league_url, self.parse_league, meta={'league_name': league_name})

        # Save the extracted league data
        with open('leagues.json', 'w') as f:
            json.dump(leagues, f, indent=4)

    def parse_league(self, response):
        """
        Parse each league's page to extract clubs.
        """
        league_name = response.meta['league_name']
        clubs = []
        
        # Scraping club links and ensuring they are Wikipedia links
        for club_link in response.xpath('//*[@class="wikitable"]/tbody/tr/td/a'):
            club_name = club_link.xpath('@title').get()
            if(club_link.xpath('@href').get() is not None):
                club_url = 'https://en.wikipedia.org' + club_link.xpath('@href').get()
            else:
                club_url = ''
            clubs.append({
                'club_name': club_name,
                'club_url': club_url
            })
            # Follow each club's link to extract player data
            yield response.follow(club_url, self.parse_club, meta={'club_name': club_name, 'league_name': league_name})
        # Scraping club links and ensuring they are Wikipedia links
        for club_link in response.xpath('//*[@class="wikitable"]/tbody/tr/td/a'):
            club_name = club_link.xpath('@title').get()
            if(club_link.xpath('@href').get() is not None):
                club_url = 'https://en.wikipedia.org' + club_link.xpath('@href').get()
            else:
                club_url = ''
            clubs.append({
                'club_name': club_name,
                'club_url': club_url
            })
            # Follow each club's link to extract player data
            yield response.follow(club_url, self.parse_club, meta={'club_name': club_name, 'league_name': league_name})
        
        # Save club data segmented by league
        league_clubs = {
            'league_name': league_name,
            'clubs': clubs
        }
        with open('clubs.json', 'a') as f:
            json.dump(league_clubs, f, indent=4)

    def parse_club(self, response):
        """
        Parse each club's page to extract player information.
        """
        club_name = response.meta['club_name']
        league_name = response.meta['league_name']
        #list of league done, list of club done, visit each club and get player list and visit each player get player details remaining
        # Scraping player information (this needs to be tailored per website structure)
        for player in response.xpath('//*[contains(@class,"football-squad")]/tbody/tr/td[4]/span/a'):
            player_url = player.xpath('@href').get()
            yield response.follow(player_url, self.parse_player_data, meta={'club_name': club_name, 'league_name': league_name})
    
    # def parse_player(self, response):

    #     club_name = response.meta['club_name']
    #     league_name = response.meta['league_name']
    #     listingUrls = []
    #     for item in response.xpath(''):
    #         listing_url = item.xpath('.//@href').extract()
    #         if listing_url and len(listing_url) > 0:
    #             absoluteUrl = getAbsoluteUrl(response.request.url, listing_url[0])
    #             yield listingUrls.append(absoluteUrl)

    #     if len(listingUrls) > 0:
    #         for url in listingUrls:
    #             yield response.follow(url=url, callback=self.parse_player_data, meta={'club_name': club_name, 'league_name': league_name})
    #             time.sleep(5)
    
    def parse_player_data(self,response):
        
        club_name = response.meta['club_name']
        league_name = response.meta['league_name']
        players = []
        player_name = response.xpath('//*[contains(@class, "infobox")]/caption/text()').get()
        player_position = response.xpath('//tr[th/text()="Position(s)"]/td/a/text()').get()
        player_age = response.xpath('//tr[th/text()="Date of birth"]/td/span').get()
        player_data = {
            'name': player_name,
            'position': player_position,
            'age': player_age
        }
        players.append(player_data)

        # Save player data segmented by league and club
        club_players = {
            'league_name': league_name,
            'club_name': club_name,
            'players': players
        }
        with open('players.json', 'a') as f:
            json.dump(club_players, f, indent=4)

