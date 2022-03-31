import scrapy


class AppSpider(scrapy.Spider):
    name = 'app'
    # allowed_domains = ['app.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        self.cates = [
            {"dispx": "1.122", "dispy": '2.222221', 'arch_id':'3820031353487263'},
            {"dispx": "1.222", "dispy": '2.2', 'arch_id':'3820028748936049'},
            {"dispx": "111111.222", "dispy": '211.2', 'arch_id':'38000000001852'},
        ]
        # item = {}
        for each in self.cates:
            item = {}
            item['dispx'] = each["dispx"]
            item['dispy'] = each["dispy"]
            item['arch_id'] = each['arch_id']
            yield item
