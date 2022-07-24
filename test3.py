
import json

from scrapy import Spider, Request, cmdline
from scrapy.cmdline import execute


class SpiderRequest(Spider):
    name = "spider_request"

    def start_requests(self):
        url = "https://httpbin.org/get?name=tom"
        yield Request(url, body=json.dumps({"age": "23"}))

    def parse(self, response):
        print(response.text)


if __name__ == '__main__':
    execute(["scrapy", "crawl", "xuke"])

