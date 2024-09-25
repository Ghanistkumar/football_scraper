from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
# import scrapy, asyncio
# from twisted.internet import asyncioreactor
# scrapy.utils.reactor.install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
# is_asyncio_reactor_installed = scrapy.utils.reactor.is_asyncio_reactor_installed()
# print(f"Is asyncio reactor installed: {is_asyncio_reactor_installed}")
from twisted.internet import reactor, defer


from musicians.spiders.FootballSpider import FootballSpider


configure_logging()
settings = get_project_settings()
runner = CrawlerRunner(settings)

#running spider sequentially
@defer.inlineCallbacks
def main():

    yield runner.crawl(FootballSpider)
    
    reactor.stop()



if __name__ == '__main__':
    main()
    reactor.run()