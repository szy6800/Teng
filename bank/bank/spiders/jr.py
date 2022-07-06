import scrapy
 # https://xkz.cbirc.gov.cn/jr/

import json
import jsonpath


class JrSpider(scrapy.Spider):
    name = 'jr'
    def start_requests(self):
        for i in range(0,50, 10):
            data = {
                "start": "{}".format(i),
                "limit":"10"
            }
            iq = 'Z'
            url ='https://xkz.cbirc.gov.cn/jr/EKXCEK/getLicence.d' \
                 'o?useState=3&organNo=&fatherOrganNo=&province=&orgAddress=&organType' \
                 '={}&branchType=&fullName=&address=&flowNo=&jrOrganPreproty='.format(iq)
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
            item['type'] = '其他金融机构'
            item['ids'] = ids
            yield item
