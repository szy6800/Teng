# -*- coding: utf-8 -*-

# @Time : 2022-08-01 13:53:45
# @Author : 石张毅
# @Site : https://bj.58.com/
# @introduce: 58同城招聘
import json
import re
import jsonpath
import scrapy
import copy
from liepin.items import LiepinJOBItem
from liepin.items import LiepinCompItem
import hashlib
from liepin.tools.DB_redis import Redis_DB
from liepin.spiders.ind_city import ind_58



class Job58Spider(scrapy.Spider):
    name = 'job_58'
    custom_settings = {
        'COOKIES_ENABLED': False,
        'DEFAULT_REQUEST_HEADERS': {'cookie': 'id58=CocG42IZ/xy9/7mLErkOAg==; 58tj_uuid=99e71191-9e21-4654-b203-8c924c2cea9c; als=0; wmda_uuid=93c07d553a63dc9df0e5bcda6f229015; gr_user_id=35f72dff-1ce3-4dae-9061-07f4b5e5594e; xxzl_deviceid=v9UYVKqMKX%2BgUwFigjqyE0I2rAO5tk1mIvcAx9JuSzSI6L%2FGxZz%2BGkIgWCWGI%2Bub; xxzl_smartid=193b68c9992ad8b78999ed9b53f74b7d; myLat=""; myLon=""; mcity=bj; __utma=253535702.1408907173.1645870892.1645870892.1661434307.2; __utmz=253535702.1661434307.2.2.utmcsr=qy.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/88642032907041/; myfeet_tooltip=end; new_uv=12; init_refer=https%253A%252F%252Fwww.baidu.com%252Fother.php%253Fsc.a00000KaRWPgMANPFInDqF3Jb3mrPaotZf3RsTPV44IIrHFAl7SpFe3J5HjLV_JEjMUAzNWCtMM-bL9sydjK5hghPAO-s-w7cNViUkT2sO2EXtRbK4t79Vv7mb6Hhl71Ay2IKGDvFM09tjUzs94IR0sdDCFPihEYFxnhdXbquxhkd15gkFKc5rDXGjOwDDuQ3U2KpszkBRzlrkgi9OTcl15ItfHI.DY_NR2Ar5Od66z3PrrW6ButVvkDj3n-vHwYxw_vU85YIMAQV8qhORGyAp7WIu8L6.TLFWgv-b5HDkrfK1ThPGujYknHb0THY0IAYqPHWPoQ5Z0ZN1ugFxIZ-suHYs0A7bgLw4TARqnsKLULFb5HR31pz1ksKzmLmqn0KdThkxpyfqnHR1rHR4njmdPfKVINqGujYkPjbvP1mYrfKVgv-b5HDkP1TLPH6Y0AdYTAkxpyfqnHc3nWm0TZuxpyfqn0KGuAnqiDF70ZKGujYk0APGujY1rH00mLFW5HfYrjf4%2526dt%253D1661568406%2526wd%253D58%2525E5%25259; spm=u-2d2yxv86y3v43nkddh1.BDPCPZ_BT; utm_source=market; sessionid=f73c1d63-ae70-4c31-a1bf-4f01d3c70b61; fzq_h=1c09b0a167f7b536b5ed19894d769698_1661568411305_d07d9c19af8048fba469910a793d5f02_3722144069; wmda_session_id_1731916484865=1661568411771-024d75ce-6490-54e8; new_session=0; wmda_session_id_11187958619315=1661568412673-b2af59dc-be49-08c9; param8616=1; param8716kop=1; wmda_visited_projects=%3B11187958619315%3B1731916484865%3B1409632296065%3B2286118353409%3B10104579731767; f=n; city=xm; 58home=xm; commontopbar_new_city_info=606%7C%E5%8E%A6%E9%97%A8%7Cxm; commontopbar_ipcity=glsanfrancisco%7C%E6%97%A7%E9%87%91%E5%B1%B1%7C1; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1661572094; fzq_js_infodetailweb=5a8e3f7c3b4079aa7112c41bb5da15d3_1661572106062_6; ppStore_fingerprint=22471D9B27FCED76F9F16C313BDB2F4DCBCDE535D1900109%EF%BC%BF1661572106411; Hm_lvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1661572107; Hm_lpvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1661572107; JSESSIONID=8CD0D4494A2C9A7678908154F504419F; fzq_js_zhaopin_list_pc=eeab7535cfed7811e0131a02e35b958c_1661572138225_7; Hm_lpvt_5bcc464efd3454091cf2095d3515ea05=1661572139; wmda_session_id_10104579731767=1661572238266-a537a872-e6d4-0505; www58com="UserID=71458147739661&UserName=0fxbux8ev"; 58cooper="userid=71458147739661&username=0fxbux8ev"; 58uname=0fxbux8ev; passportAccount="atype=0&bstate=0"; PPU=UID=71458147739661&UN=0fxbux8ev&TT=21195cc56ca2bdab77c812d962d66877&PBODY=Lo6z1fLVtp9EGIO6KxN5W5_hfwKqO5QijLA4YrEPau9csSMV48m3L_iJi3nMYYH7NEZs9CO_EwjDhxtYiI84Q7csHJM9tDpyuO4qpkWyV-PymuYHZNw2LFWSgoFriPJys0p64dMc5hJhHJP7JsXf2Xq2UP3NicM85KQY00HRsnI&VER=1&CUID=Ia5GM2c1i47263wLL87x3w; xxzl_cid=53e07ae5dadb4c80ad22a4f7e6ae5fdb; xzuid=b3031ea2-a74f-473b-aa0c-c2b45d0562ac; jobBottomBar=1', 'if-modified-since': 'Wed, 24 Aug 2022 08:45:21 GMT', 'if-none-match': 'W/"108470-1661330721000"', 'referer': 'https://xm.58.com/?PGTID=0d000000-0000-036e-9a9b-443d11b355d2&ClickID=1&pts=1661572299792', 'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-origin', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    }

    def start_requests(self):
        url = 'https://bj.58.com/yingjiangong/pn9/?pid=454607466785308672&PGTID=0d302f81-0000-17be-07d9-5eec830f26fe&ClickID=3'
        yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    # 岗位列表解析
    def parse(self, response, *args, **kwargs):
        count_list = response.xpath('//*[@id="list_con"]/li')
        if count_list is []:
            return
        for count in count_list:
            item = LiepinJOBItem()
            # link_id = count.xpath('.//*[@class="item_con apply"]/@infoid').get()
            cate = count.xpath('.//div[@class="job_name clearfix"]/a/@href').get()
            item['link'] = re.findall('https://bj.58.com/.*?shtml?',cate)[0]
            # print(item['link'])
            item['source'] = '58同城'
            item['base'] = ''
            item['pub_time'] = ''
            item['job_title'] = count.xpath('.//*[@class="job_require"]/span[@class="cate"]/text()').get()
            # 学历
            item['education'] = count.xpath('.//*[@class="job_require"]/span[@class="xueli"]/text()').get()
            # 工作年限
            item['work_years'] = count.xpath('.//*[@class="job_require"]/span[@class="jingyan"]/text()').get()

            salary = count.xpath('.//p[@class="job_salary"]/text()').get()
            if '面议' in salary:
                item['salary'] = salary
            else:
                item['salary'] = salary+'元/月'
            item['job_indu'] = ''
            company_item = LiepinCompItem()

            company_item['comp_link'] = count.xpath('.//*[@class="comp_name"]/a/@href').get()
            uid = item['link'] + item['job_title']+item['salary']
            item['uid'] = hashlib.md5(uid.encode(encoding='utf-8')).hexdigest()
            if Redis_DB().redis_job(item['uid']) is True:  # 数据去重
                print(item['job_title'], item['link'], '\033[0;35m <=======此岗位已采集=======> \033[0m')
                continue
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item),
                                                                               'company_item': copy.deepcopy(company_item)},
                                 dont_filter=True)

    # 岗位详情信息
    def parse_info(self,response):
        # print(response.url)
        # print(response.text)
        if response.status != 200:
            return
        item = response.meta['item']
        # 岗位要求
        item['job_desc'] = ''.join(response.xpath('//*[@class="des"]//text()').getall())
        # 公司item
        company_item = response.meta['company_item']

        company_item['comp_desc'] = ''.join(response.xpath('//*[@class="comIntro"]//text()').getall())
        # 福利
        company_item['welfare'] = '|'.join(response.xpath('//*[@class="pos_welfare"]/span/text()').getall())
        item['city'] = response.xpath('//*[@class="pos_area_item"][1]/text()').get()
        item['job_tags'] = ''
        # 公司json链接
        ids = re.findall('https://qy.58.com/(.*?)/',company_item['comp_link'])[0]
        comp_href = f'https://qy.58.com/data/ent/detail/{ids}'
        # 企业sign 判断是否是名企 然后对链接进行处理
        sign = ''.join(response.xpath('//*[@class="baseInfo_sign"]/i/@title').getall())
        if '名企-58同城已认证' in sign:
            # 名企的链接
            company_item['link'] = response.url
            company_item['name'] = response.xpath('//*[@class="intro_middle"]/h3/text()|//*[@class="pos_title"]/text()').get()
            # 社会统一代码
            company_item['comp_code'] = ''
            # 登记机关
            company_item['reg_au'] = ''
            # 法人代表
            company_item['legal_peo'] = ''
            # 经营状态
            company_item['status'] = ''
            # 所在地
            company_item['locations'] = ''
            # 企业类型
            company_item['comp_type'] = response.xpath('//*[@class="comp_baseInfo_link"]/text()').get()
            company_item['lng'] =re.findall('"lon"[:： \n]"(.*?)"[,}]+',response.text)[0]
            company_item['lat'] = re.findall('"lat"[:： \n]"(.*?)"[,}]+',response.text)[0]
            company_item['comp_website'] = ''
            company_item['comp_addr'] = ''.join(response.xpath('//*[@class="pos-area"]//text()').getall()).replace('查看地图','')
            # 注册时间
            company_item['reg_time'] = ''
            # 注册资本
            company_item['reg_capi'] = ''
            # 经营期限
            company_item['op_period'] = ''
            # 经营范围
            company_item['man_range'] = ''
            company_item['comp_ind'] = ''
            company_item['fig_stage'] = ''
            company_item['num_of_peo'] = response.xpath('//*[@class="comp_baseInfo_scale"]/text()').get()
            company_item['logo'] = ''
            cid = company_item['name'] + company_item['comp_code']
            company_item['cid'] = hashlib.md5(cid.encode(encoding='utf-8')).hexdigest()
            item['cid'] = company_item['cid']
            item['comp_name'] = company_item['name']
            yield item
            yield company_item
        else:
            yield scrapy.Request(comp_href,
                                 callback=self.com_info,
                                 meta={'item': copy.deepcopy(item),'company_item': copy.deepcopy(company_item)},
                                 dont_filter=True)

    # 普通公司的信息解析
    def com_info(self, response):
        company_item = response.meta['company_item']
        item = response.meta['item']
        json_text = json.loads(response.text)
        # 公司名字
        company_item['name'] = jsonpath.jsonpath(json_text, '$..entName')[0]
        # 社会统一代码
        company_item['comp_code'] = jsonpath.jsonpath(json_text, '$..creditCode')[0]
        # 登记机关
        company_item['reg_au'] = jsonpath.jsonpath(json_text, '$..orgApprovedInstitute')[0]
        # 法人代表
        company_item['legal_peo'] = jsonpath.jsonpath(json_text, '$..legalPersonName')[0]
        # 经营状态
        company_item['status'] = jsonpath.jsonpath(json_text, '$..regStatus')[0]
        # 所在地
        company_item['locations'] =jsonpath.jsonpath(json_text, '$..cityfullName')[0]
        # 企业类型
        company_item['comp_type'] = jsonpath.jsonpath(json_text, '$..companyType')[0]

        lng = jsonpath.jsonpath(json_text, '$..axis')[0]
        if lng is None:
            company_item['lng'] = ''
            company_item['lat'] = ''
        else:
            company_item['lng'] = lng.split(',')[0]
            company_item['lat'] = lng.split(',')[1]
        company_item['comp_website'] = jsonpath.jsonpath(json_text, '$..email')[0]

        company_item['comp_addr'] = jsonpath.jsonpath(json_text, '$..regLocation')[0]
        # 注册时间
        company_item['reg_time'] = jsonpath.jsonpath(json_text, '$..createTime')[0]
        # 注册资本
        company_item['reg_capi'] = jsonpath.jsonpath(json_text, '$..regCapital')[0]
        # 经营期限
        company_item['op_period'] = ''
        # 经营范围
        company_item['man_range'] = jsonpath.jsonpath(json_text, '$..businessScope')[0]

        company_item['comp_ind'] = jsonpath.jsonpath(json_text, '$..industryText')[0]
        #1
        company_item['fig_stage'] = ''

        company_item['num_of_peo'] = jsonpath.jsonpath(json_text, '$..sizeText')[0]

        company_item['link'] = response.url
        logo = jsonpath.jsonpath(json_text, '$..enterpriseLogoUrl')[0]
        if logo is None:
            company_item['logo'] = ''
        else:
            company_item['logo'] = f'https://pic1.58cdn.com.cn/{logo}'
        cid = company_item['name'] + company_item['comp_code']
        company_item['cid'] = hashlib.md5(cid.encode(encoding='utf-8')).hexdigest()
        item['cid'] = company_item['cid']
        item['comp_name'] = company_item['name']

        yield item
        yield company_item









