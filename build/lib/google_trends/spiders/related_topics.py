# -*- coding: utf-8 -*-
import scrapy
import pdb
from pytrends.request import TrendReq
import json


class RelatedTopicsItem(scrapy.Item):
    search_term = scrapy.Field()
    search_phrase = scrapy.Field()
    top = scrapy.Field()
    breakout = scrapy.Field()


class RelatedTopicsSpider(scrapy.Spider):
    name = 'related_topics'

    # def __init__(self, search_term='cybersecurity', start_date='2020-04-29', end_date='2020-05-26', cat=0, geo='', gprop=''):
    def __init__(self, search_term='', start_date=None, end_date=None, cat=0, geo='', gprop=''):
        self.search_term = search_term
        self.start_date = start_date
        self.end_date = end_date
        self.cat = cat
        self.geo = geo
        self.gprop = gprop

    def start_requests(self):
        yield scrapy.Request('https://www.google.com', callback=self.parse)

    def parse(self, response):
        try:
            pytrends = TrendReq(hl='en-US', tz=360)
            pytrends.build_payload(
                self.search_term.split('|||'), cat=self.cat,
                timeframe='{} {}'.format(self.start_date, self.end_date),
                geo=self.geo,
                gprop=self.gprop)
            df = pytrends.related_topics()

            keys = ['rising', 'top']
            for key in keys:
                json_data = json.loads(
                    df[self.search_term][key].to_json(orient="table"))

                for item in json_data['data']:
                    for search_term in self.search_term.split('|||'):
                        yield RelatedTopicsItem(
                            search_term=search_term,
                            search_phrase=item['topic_title'],
                            top=item['formattedValue'] if key == 'top' else '',
                            breakout=item['formattedValue'] if key == 'rising' else ''
                        )
        except Exception as e:
            print(e)
            pass
