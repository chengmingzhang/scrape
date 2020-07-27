import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from biquge.items import BiqugeItem


class Biquge98Spider(CrawlSpider):
    name = 'biquge98'
    allowed_domains = ['biquge98.com']
    start_urls = ['https://www.biquge98.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@id="pagelink"]/a[@class="next"]')),
        Rule(LinkExtractor(allow=r'https://www\.biquge98\.com/x[a-z]+/$')),
        Rule(LinkExtractor(restrict_xpaths="//div[@class='l']/ul/li/span[1]"), callback='parse_item'),
    )

    def parse_item(self, response):
        item = BiqugeItem()
        item['detail_url'] = response.url
        item['name'] = response.xpath("//h1/text()").extract_first()
        item['cover_img'] = response.xpath("//div[@id='fmimg']/img/@src").extract_first()
        item['author'] = response.xpath("//div[@id='info']/p[1]/a/text()").extract_first()
        item['introduce'] = response.xpath("//div[@id='intro']/p/text()").extract_first()
        yield item
