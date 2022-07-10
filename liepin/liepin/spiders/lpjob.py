
import scrapy
import json
import jsonpath
import copy


class LpjobSpider(scrapy.Spider):
    name = 'lpjob'

    def __init__(self, *args, **kwargs):
        super(LpjobSpider, self).__init__()
        # self.result = dbz()

    def start_requests(self):
        url = 'https://www.liepin.com/job/1948460657.shtml?d_sfrom=search_prime&d_ckId=a2322434ded38308d5b041ee68056b90&d_curPage=1&d_pageSize=40&d_headId=a2322434ded38308d5b041ee68056b90&d_posi=38&skId=x86aktwr2t7vsbbus26hteiagkgxq0i9&fkId=x86aktwr2t7vsbbus26hteiagkgxq0i9&ckId=ulb2bf4t2gwaf97suycz7xxswxoj8dp8&sfrom=search_job_pc&curPage=1&pageSize=40&index=38'
        item = {}

        yield scrapy.Request(url, callback=self.parse, dont_filter=True,
                             meta={'item': copy.deepcopy(item)})

    def parse(self, response, *args, **kwargs):
        print(response.text)
