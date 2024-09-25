# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
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
