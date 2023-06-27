import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        for tr in response.xpath('//*[@id="numerical-index"]//tbody/tr'):
            number = tr.css('td:nth-child(2) a::text').get()
            name = tr.css('td:nth-child(3) a::text').get()
            pep_link = tr.css('td:nth-child(3) a::attr(href)').get()
            yield response.follow(
                pep_link,
                meta={'number': number, 'name': name},
                callback=self.parse_pep
            )

    def parse_pep(self, response):
        status = response.css('dt:contains("Status") + dd abbr::text').get()
        data = {
            'number': response.meta['number'],
            'name': response.meta['name'],
            'status': status
        }
        yield PepParseItem(data)
