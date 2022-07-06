import scrapy
import json
import jsonpath


class ZjSpider(scrapy.Spider):
    name = 'zj'

    def start_requests(self):
        for i in range(0, 500,10):
            data = {
                "start": "{}".format(i),
                "limit":"10"
            }
            a1='2'
            url ='https://xkz.cbirc.gov.cn/zj/EKXEKX/getLicence.do?useState=3&organNo=&fatherOrganN' \
                 'o=&province=&organType={}&fullName=&address=&flowNo='.format(a1)
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
        useState = jsonpath.jsonpath(json_text,'$..id')
        endDate = jsonpath.jsonpath(json_text,'$..endDate')
        for certCode,date,flowNo,fullName,setDate,useState,endDate in zip(certCode,date,flowNo,fullName,setDate,useState,endDate):
            item = {}
            item['certCode'] = certCode
            item['dates'] = date
            item['flowNo'] = flowNo
            item['fullName'] = fullName
            item['setDate'] = setDate
            item['ids'] = useState
            item['type'] = '保险经纪公司'
            item['endDate'] = endDate

            yield item

