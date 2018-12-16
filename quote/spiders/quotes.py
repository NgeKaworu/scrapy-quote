# -*- coding: utf-8 -*-
import scrapy
import time
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

        for author in response.css('.next').xpath('a/@href'):
            yield response.follow(author, callback=self.parse)

        for about in response.css('.author').xpath('../a/@href'):
            yield response.follow(about, callback=self.parseAbout)

    def parseAbout(self, response):
        item = QuoteItem()
        detail = response.css('.author-details')
        title = detail.css('.author-title::text').extract_first().strip()
        description = detail.css(
            '.author-description::text').extract_first().strip()
        item['about'] = { 'title': title, 'description': description }
        yield item
