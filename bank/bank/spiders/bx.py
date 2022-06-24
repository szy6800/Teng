import scrapy

# https://xkz.cbirc.gov.cn/bx/ 保险许可证信息

import json
import jsonpath

class BxSpider(scrapy.Spider):
    name = 'bx'
    # allowed_domains = ['baidu.com']
    # start_urls = ['http://baidu.com/']

    def start_requests(self):
        for i in range(0,20,10):
            data = {
                "start": "{}".format(i),
                "limit":"10"
            }
            a1 = '3'
            a2 = '8'
            a3 = ''
            url = 'https://xkz.cbirc.gov.cn/bx/CEKgQq/getLicence.do?useState={}&orga' \
                  'nNo=&fatherOrganNo=&organType={}' \
                  '&branchType={}&orgLevel=&fullName=&a' \
                  'ddress=&flowNo='.format(a1,a2,a3)
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
        useState = jsonpath.jsonpath(json_text,'$..useState')
        for certCode,date,flowNo,fullName,setDate,useState in zip(certCode,date,flowNo,fullName,setDate,useState):
            item = {}
            item['certCode'] = certCode
            item['dates'] = date
            item['flowNo'] = flowNo
            item['fullName'] = fullName
            item['setDate'] = setDate
            item['useState'] = useState
            item['type'] = '其他'
            yield item
