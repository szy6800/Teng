import scrapy
 # https://xkz.cbirc.gov.cn/jr/

import json
import jsonpath
class JrSpider(scrapy.Spider):
    name = 'jr'
    def start_requests(self):
        for i in range(0, 50,10):
            data = {
                "start": "{}".format(i),
                "limit":"10"
            }
            a1='Z'
            url ='https://xkz.cbirc.gov.cn/jr/CEKQqR/getLicence.do?useState=3&organNo=&' \
                 'fatherOrganNo=&province=&orgAddress=&organType={}&branchType=&fullName=&ad' \
                 'dress=&flowNo=&jrOrganPreproty='.format(a1)
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
            item['type'] = '其他金融机构'
            yield item
