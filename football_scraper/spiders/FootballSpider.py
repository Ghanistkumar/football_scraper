import scrapy
import json

class FootballSpider(scrapy.Spider):
    name = 'football'
    
    # Starting URL (English football league system on Wikipedia)
    start_urls = ['https://en.wikipedia.org/wiki/English_football_league_system']

    def parse(self, response):

        """
        Parse the Wikipedia page to extract league names and URLs.
        """
        leagues = []
        for row in response.xpath('//*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr')[1:]:  # Skipping header row
            league_name = row.xpath('//td[3]/p/b/a').get()
            league_url = row.xpath('//td[3]/p/b/a/@href').get()

            # Only proceed if both league_name and league_url are found
            if league_name and league_url:
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
        
        # Scraping club links
        for club_link in response.css('a::attr(href)').getall():
            club_name = response.css('a::text').get()
            club_url = response.urljoin(club_link)
            if club_url:
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
        players = []

        # Scraping player information (this needs to be tailored per website structure)
        for player in response.css('div.player-info'):
            player_name = player.css('span.player-name::text').get()
            player_position = player.css('span.player-position::text').get()
            player_age = player.css('span.player-age::text').get()
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
