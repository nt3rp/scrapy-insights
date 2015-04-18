# -*- coding: utf-8 -*-
import json
import scrapy
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

    def __init__(self, token='CAAUWHeiuLx0BAEZB4WO5fGnf59YDT5fWHvo4caTrVUMCjLeFZB3AiB3lJanc3pI9KEGLTyaZBtZBUyn34CiidvghnbEH2yKS81sm5p3PfHGNzy13VZAfx9WImHUuBGqtZCb61XA63pxD31WlzTh27vMZBNVZCDTdDh7T9rXr6JceZB690LiKng33mxIkyUj8x04CR0LJNZCosURj0cuVaHNzFkkshq3inSMJbhsJZBFefIyywZDZD', page_id='1613996332147163', *args, **kwargs):
        assert token is not None, 'Token required to make Facebook request'
        assert page_id is not None, 'Page Id needed to make Facebook request'

        self.token = token
        self.page_id = page_id

        # TODO: What defines 'recent' posts?
        self.start_urls = [
            'https://graph.facebook.com/v2.3/{page_id}/posts?access_token={token}'.format(
                token=token, page_id=page_id
            )
        ]

    def parse(self, response):
        # TODO: Do we want to page through results?
        try:
            page = json.loads(response.body)
        except:
            pass

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
        insight['post_url'] = first(post.get('actions'), {}).get('link')        # Url / Link
        insight['post_headline'] = post.get('name', 'Status Update')          # Headline
        insight['post_blurb'] = post.get('description', post.get('message'))  # Blurb

        pass

    @staticmethod
    def flatten_values(insight_values):
        if not insight_values:
            return 0

        return next((i.get('value') for i in insight_values if i.get('value')), 0)