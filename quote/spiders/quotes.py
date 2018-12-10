# -*- coding: utf-8 -*-
import scrapy, time
from quote.items import QuoteItem



class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        item = QuoteItem()
        for author in response.css('.author::text'):
            item['author'] = author.extract()
            yield item

        for href in response.css('.next').xpath('a/@href'):
            yield response.follow(href, callback=self.parse)
