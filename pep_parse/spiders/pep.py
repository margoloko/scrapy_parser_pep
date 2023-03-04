import scrapy
from datetime import datetime as dt
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = ["http://peps.python.org/"]

    def parse(self, response):
        for href in response.css('section.numerical-index td a::attr(href)'):
            yield response.follow(href, callback=self.parser_pep)

    def parser_pep(self, response):
        data = {
            'number': response.css(
            'h1::text').re_first(r'PEP (?P<number>\d+)').get().group('number'),
            'name': response.css(
            'h1::text').re_first(r'\W (?P<name>\D+ .*)').getall().group('name'),
            'status': response.css(
                    'dt:contain("Status") + dd *::text').get(), }
        yield PepParseItem(data)
