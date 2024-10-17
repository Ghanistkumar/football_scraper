# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags
from football_scraper.helpers.scraper_handler import remove_html_tags, remove_newline_tab, extractDatefromString, image_url_handler, remove_style_tags, get_wiki_id, split_data, string_to_lowercase, remove_white_spaces


class FootballScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # wiki_url = scrapy.Field(
    #     output_processor = TakeFirst()
    # )
    # football_league_wiki_id = scrapy.Field(
    #     input_processor = MapCompose(get_wiki_id),
    #     output_processor = TakeFirst()
    # )
    # league_image_url = scrapy.Field(
    #     input_processor = MapCompose(image_url_handler)
    # )
    # leagueName = scrapy.Field(
    #     input_processor = MapCompose(remove_html_tags, remove_newline_tab),
    #     output_processor = TakeFirst()
    # )
    pass
class LeaguesItem(scrapy.Item):

    league_wiki_id = scrapy.Field(
        input_processor = MapCompose(get_wiki_id),
        output_processor = TakeFirst()
    )
    # Field for title of the league
    league_url = scrapy.Field(
        output_processor = TakeFirst()
    )
    title = scrapy.Field(
        input_processor = MapCompose(remove_style_tags, remove_html_tags),
        output_processor = TakeFirst()
    )

    # Field for league logo
    logo = scrapy.Field(
        input_processor = MapCompose(image_url_handler, remove_html_tags),
        output_processor = TakeFirst()
    )
    
    # Field for country
    country = scrapy.Field(
        input_processor = MapCompose(remove_style_tags, remove_html_tags),
        output_processor = TakeFirst()
    )
    
    # Field for region
    region = scrapy.Field(
        input_processor = MapCompose(remove_style_tags, remove_html_tags),
        output_processor = TakeFirst()
    )

    no_of_teams = scrapy.Field(
        input_processor = MapCompose(remove_style_tags, remove_html_tags),
        output_procesoor = TakeFirst()
    )

    current_champions = scrapy.Field(
        input_processor = MapCompose(remove_style_tags, remove_html_tags),
        output_procesoor = TakeFirst()
    )

    # Field for season list (as a list of dicts)
    season_list = scrapy.Field(
        input_processor = MapCompose(),
    )

class ClubsItem(scrapy.Item):

    club_wiki_id = scrapy.Field(
        input_processor = MapCompose(get_wiki_id),
        output_processor = TakeFirst()
    )

    # Field for club title
    title = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    nickname = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for description (removing HTML tags)
    description = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )

    # Field for inception date
    inception_date = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    chairman = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    manager = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    league = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    ground = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for mobile number
    mobile = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for Instagram profile URL
    insta_profile = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for LinkedIn profile URL
    linkedin_profile = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for Twitter profile URL
    twitter_profile = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for website URL
    website_url = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for post code
    post_code = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for address
    address = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for country
    country = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for state
    state = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for city
    city = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for zipcode
    zipcode = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for logo URL
    logo = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for league list (as a list of dicts)
    league_list = scrapy.Field(
        input_processor = MapCompose(),
    )
class PlayersItem(scrapy.Item):

    player_wiki_id = scrapy.Field(
        input_processor = MapCompose(get_wiki_id),
        output_processor = TakeFirst()
    )

    # Field for first name
    first_name = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for last name
    last_name = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for date of birth
    date_of_birth = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for gender
    gender = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for country dialling code
    country_dialling_code = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for country code alpha
    country_code_alpha = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for mobile number
    mobile = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for height
    height = scrapy.Field(
        input_processor = MapCompose(float),
        output_processor = TakeFirst()
    )

    # Field for weight
    weight = scrapy.Field(
        input_processor = MapCompose(float),
        output_processor = TakeFirst()
    )

    # Field for dominant foot
    dominant_foot = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for player position
    position = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for current club
    current_club = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for player logo (URL)
    logo = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for description (removing HTML tags)
    description = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )

    # Field for Instagram profile URL
    insta_profile = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for LinkedIn profile URL
    linkedin_profile = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for Twitter profile URL
    twitter_profile = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for website URL
    website_url = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for post code
    post_code = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for address
    address = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for country
    country = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for state
    state = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for city
    city = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for zipcode
    zipcode = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )

    # Field for player statistics (list of dicts)
    player_statistics = scrapy.Field(
        input_processor = MapCompose()
    )