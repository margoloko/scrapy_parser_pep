import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        for pep in response.css('section#numerical-index td a::attr(href)'):
            yield response.follow(pep, callback=self.parse_pep)

    def parse_pep(self, response):

        yield PepParseItem({
            'number': response.css('h1::text').re_first(r'PEP (?P<number>\d+)'
                                                        ),
            'name': response.css('h1::text').re_first(r'\W (?P<name>\D+ .*)'
                                                      ),
            'status': response.css('dt:contains("Status") + dd::text').get()})
