# -*- coding: utf-8 -*-
import scrapy
import pdb
from pytrends.request import TrendReq
import json


class InterestOverTimeItem(scrapy.Item):
    search_term = scrapy.Field()
    date = scrapy.Field()
    interest = scrapy.Field()
    geo = scrapy.Field()


class InterestOverTimeSpider(scrapy.Spider):
    name = 'interest_over_time'

    def __init__(self, search_term='cybersecurity|||rsaconference.com', start_date='2020-04-29', end_date='2020-05-26', cat=0, geo='US|||SG', gprop=''):
    # def __init__(self, search_term='', start_date=None, end_date=None, cat=0, geo='', gprop=''):
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
            for geo in self.geo.split('|||'):
                pytrends = TrendReq(hl='en-US', tz=360)
                pytrends.build_payload(
                    self.search_term.split('|||'), cat=self.cat,
                    timeframe='{} {}'.format(self.start_date, self.end_date),
                    geo=geo,
                    gprop=self.gprop)
                df = pytrends.interest_over_time()

                json_data = json.loads(df.to_json(orient="table"))

                for item in json_data['data']:
                    for search_term in self.search_term.split('|||'):
                        yield InterestOverTimeItem(
                            search_term=search_term,
                            date=item['date'].split('T')[0],
                            interest=item[search_term],
                            geo=geo
                        )
        except Exception as e:
            print(e)
            pass
