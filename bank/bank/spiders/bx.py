import scrapy

# https://xkz.cbirc.gov.cn/bx/ 保险许可证信息

import json
import jsonpath

class BxSpider(scrapy.Spider):
    name = 'bx'
    # allowed_domains = ['baidu.com']
    # start_urls = ['http://baidu.com/']

    def start_requests(self):
        for i in range(0,40,10):
            data = {
                "start": "{}".format(i),
                "limit":"10"
            }
            url = 'https://xkz.cbirc.gov.cn/bx/EKXEKX/getLicence.do?useState=3&organNo=&fatherOrganNo=&organType=8&branchType=&orgLevel=&fullName=&address=&flowNo='
            yield scrapy.FormRequest(url=url, formdata=data, method='POST',callback=self.parse)


    def parse(self, response, *args):
        # print(response.text)
        json_text = json.loads(response.text)
        # print(json_text)
        certCode = jsonpath.jsonpath(json_text,'$..certCode')
        # print(certCode)
        date = jsonpath.jsonpath(json_text,'$..date')
        flowNo = jsonpath.jsonpath(json_text,'$..flowNo')
        fullName = jsonpath.jsonpath(json_text,'$..fullName')
        setDate = jsonpath.jsonpath(json_text,'$..setDate')
        ids = jsonpath.jsonpath(json_text,'$..id')
        for certCode, date, flowNo, fullName,setDate, ids in \
                zip(certCode,date,flowNo,fullName,setDate,ids):
            item = {}
            item['certCode'] = certCode
            item['dates'] = date
            item['flowNo'] = flowNo
            item['fullName'] = fullName
            item['setDate'] = setDate
            item['type'] = '资产管理'
            item['ids'] = ids
            yield item
