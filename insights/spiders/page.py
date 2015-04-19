# -*- coding: utf-8 -*-
import json
import scrapy
from insights.items import InsightsItem
from insights.utils import first


class PageSpider(scrapy.Spider):
    name = 'page'
    allowed_domains = ['graph.facebook.com']
    token = ''

    insights_keys = [
        'post_impressions_organic',              # Organic Impressions (Total)
        'post_impressions_organic_unique',       # Organic Impressions (Unique)
        'post_impressions_organic_paid',         # Paid Impressions (Total)
        'post_impressions_organic_paid_unique',  # Paid Impressions (Unique)
        'post_engaged_users',                    # Link Clicks
        'post_engaged_fans',                     # Likes
        'post_stories',                          # Links
        'post_story_adds'                        # Comments
    ]

    def __init__(self, token=None, page=None, *args, **kwargs):
        self.token = token
        self.page_id = page

        self.start_urls = [
            'https://graph.facebook.com/v2.3/{page_id}/posts?access_token={token}'.format(
                token=token, page_id=page
            )
        ]

    def parse(self, response):
        try:
            page = json.loads(response.body)
        except:
            yield

        posts = page['data']

        for post in posts:
            url = 'https://graph.facebook.com/v2.3/{0}/insights?access_token={1}'.format(post['id'], self.token)
            request = scrapy.Request(url, callback=self.parse_insights)
            request.meta['post'] = post
            yield request

    def parse_insights(self, response):
        insights_response = json.loads(response.body)

        # TODO: Deal with paging
        insights = insights_response.get('data')

        # Convert to dictionary
        insight = dict((i.get('name'), self.flatten_values(i.get('values'))) for i in insights)

        # Only keep desired keys
        insight = dict((key, insight.get(key)) for key in self.insights_keys)

        post = response.meta.get('post')
        insight['post_url'] = first(post.get('actions'), {}).get('link')      # Url / Link
        insight['post_headline'] = post.get('name', 'Status Update')          # Headline
        insight['post_blurb'] = post.get('description', post.get('message'))  # Blurb

        yield InsightsItem(insight)

    @staticmethod
    def flatten_values(insight_values):
        if not insight_values:
            return 0

        return next((i.get('value') for i in insight_values if i.get('value')), 0)