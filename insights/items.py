# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InsightsItem(scrapy.Item):
    post_url                             = scrapy.Field()  # Link / URL
    post_headline                        = scrapy.Field()  # Headline
    post_blurb                           = scrapy.Field()  # Blurb
    post_impressions_organic             = scrapy.Field()  # Organic Impressions (Total)
    post_impressions_organic_unique      = scrapy.Field()  # Organic Impressions (Unique)
    post_impressions_organic_paid        = scrapy.Field()  # Paid Impressions (Total)
    post_impressions_organic_paid_unique = scrapy.Field()  # Paid Impressions (Unique)
    post_engaged_users                   = scrapy.Field()  # Link Clicks
    post_engaged_fans                    = scrapy.Field()  # Likes
    post_stories                         = scrapy.Field()  # Links
    post_story_adds                      = scrapy.Field()  # Comments
