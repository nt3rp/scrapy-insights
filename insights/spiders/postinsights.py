# -*- coding: utf-8 -*-
import scrapy


class PostInsightsSpider(scrapy.Spider):
    name = "postinsights"
    allowed_domains = ["facebook.com"]
    start_urls = (
        'http://www.facebook.com/',
    )

    def parse(self, response):
        pass
