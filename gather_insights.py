import sys

from twisted.application.service import Process
from twisted.internet import reactor, task
from scrapy.crawler import Crawler
from scrapy import log
from insights.spiders.page import PageSpider
from scrapy.utils.project import get_project_settings

class UrlCrawlerScript(Process):
    def __init__(self, spider):
        Process.__init__(self)
        settings = get_project_settings()
        self.crawler = Crawler(settings)

        if not hasattr(self, 'crawler'):
            self.crawler.install()
            self.crawler.configure()
        self.spider = spider

    def run(self):
        self.crawler.crawl(self.spider)
        self.crawler.start()


def run_spider(token="", page=""):
    spider = PageSpider(token=token, page=page)
    crawler = UrlCrawlerScript(spider)
    crawler.run()


if __name__ == "__main__":
    token = sys.argv[1]
    page = sys.argv[2]

    l = task.LoopingCall(run_spider, token=token, page=page)

    timeout_seconds = 5.0
    l.start(timeout_seconds)

    log.start()
    reactor.run()
