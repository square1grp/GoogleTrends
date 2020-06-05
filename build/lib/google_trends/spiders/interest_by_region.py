# -*- coding: utf-8 -*-
import scrapy
import pdb
from pytrends.request import TrendReq
import json


class InterestByRegionItem(scrapy.Item):
    search_term = scrapy.Field()
    country = scrapy.Field()
    interest = scrapy.Field()


class InterestByRegionSpider(scrapy.Spider):
    name = 'interest_by_region'

    # def __init__(self, search_term='cybersecurity|||rsa conference|||blackhat', start_date='2020-04-01', end_date='2020-05-31', cat=0, geo='', gprop=''):
    def __init__(self, search_term='', start_date=None, end_date=None, cat=0, geo='', gprop=''):
        self.search_term = search_term
        self.start_date = start_date
        self.end_date = end_date
        self.cat = cat
        self.geo = ''
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
            df = pytrends.interest_by_region()

            json_data = json.loads(df.to_json(orient="table"))

            for item in json_data['data']:
                for search_term in self.search_term.split('|||'):
                    yield InterestByRegionItem(
                        search_term=search_term,
                        country=item['geoName'].split('T')[0],
                        interest=item[search_term]
                    )
        except Exception as e:
            print(e)
            pass
