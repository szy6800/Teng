
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
        url = 'https://www.liepin.com/job/1950541367.shtml?d_sfrom=search_prime&d_ckId=c8bacda51229410b03af09b1bf59e17f&d_curPage=0&d_pageSize=40&d_headId=a2322434ded38308d5b041ee68056b90&d_posi=39&skId=x86aktwr2t7vsbbus26hteiagkgxq0i9&fkId=1nx6i9vjkm6s2q38akyfpsk9qf8pwa3a&ckId=1nx6i9vjkm6s2q38akyfpsk9qf8pwa3a&sfrom=search_job_pc&curPage=0&pageSize=40&index=39'
        item = {}

        yield scrapy.Request(url, callback=self.parse, dont_filter=True,
                             meta={'item': copy.deepcopy(item)})

    def parse(self, response, *args, **kwargs):
        print(response.text)
