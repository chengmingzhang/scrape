import scrapy
from doutu.items import DoutuItem


class Doutu1Spider(scrapy.Spider):
    name = 'doutu1'
    allowed_domains = ['doutula.com']
    start_urls = ['https://www.doutula.com/photo/list/?page=1']

    def parse(self, response):
        lis = response.xpath('//div[@class="page-content text-center"]//a')
        for li in lis:
            item = DoutuItem()
            item['name'] = li.xpath("./img/@alt").extract_first()
            item['image_urls'] = li.xpath("./img/@data-original").extract_first()
            yield item
        MAX_PAGES = self.settings['MAX_PAGES']
        for page in range(2, MAX_PAGES):
            url = "https://www.doutula.com/photo/list/?page=%d" % page
            yield scrapy.Request(url, callback=self.parse)