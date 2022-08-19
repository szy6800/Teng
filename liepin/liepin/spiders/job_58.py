# -*- coding: utf-8 -*-

# @Time : 2022-08-01 13:53:45
# @Author : 石张毅
# @Site : https://bj.58.com/
# @introduce: 58同城招聘
import re

import scrapy
import copy
from liepin.items import LiepinJOBItem
from liepin.items import LiepinCompItem
import hashlib
from liepin.tools.DB_redis import Redis_DB
from liepin.spiders.ind_city import liepin_ind



class Job58Spider(scrapy.Spider):
    name = 'job_58'
    custom_settings = {
        'COOKIES_ENABLED': False,
        'DEFAULT_REQUEST_HEADERS': {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://bj.58.com/yingjiangong/pn2/?pid=454607466785308672&PGTID=0d302f81-0000-17be-07d9-5eec830f26fe&ClickID=3",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            "cookie":'id58=CocHKmJrsvwd00/gBFPwAg==; 58tj_uuid=883f06af-ea1f-4366-8018-3e35725400e7; als=0; wmda_uuid=22af24eb753314591c43d6563191d5af; wmda_new_uuid=1; xxzl_deviceid=wb8gy%2FPMsMYQmw%2BwB5TZAOoxa%2B0WEbhPnxMTVNdk5HUwxd%2BheF7itHNXY97solAH; 58home=bj; myfeet_tooltip=end; xxzl_smartid=610a42d76847430ba91d9f85189542fc; Hm_lvt_fe7700af2f35759e6256aa5635b9c9ff=1659340591; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1659340632; final_history=47907462014755; myLat=""; myLon=""; mcity=bj; city=bj; f=n; sessionid=6c5fa5b7-49e1-47e8-b229-70c73c45c165; Hm_lvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1660098484,1660204241,1660289005,1660543846; fzq_h=28f0ac6d9bc123ded3d3ee10abd7c55a_1660632083226_ffca48b5879648e9a142fcc51ea1f546_2071877498; utm_source=; new_uv=19; init_refer=; spm=; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; commontopbar_ipcity=bj%7C%E5%8C%97%E4%BA%AC%7C0; new_session=0; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1660098019,1660204140,1660283975,1660632208; __utma=253535702.71241368.1656061471.1659331880.1660637082.4; __utmc=253535702; __utmz=253535702.1660637082.4.4.utmcsr=qy.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/86367446243348/; wmda_session_id_1731916484865=1660640994570-2303badb-f35c-b251; wmda_session_id_11187958619315=1660641005064-6ca28da9-5531-ed2c; xxzl_cid=82d0de8097ae4b218bb0cf7518483a55; xzuid=580970d0-7108-4f94-84a5-72a409098990; wmda_visited_projects=%3B11187958619315%3B1731916484865%3B2286118353409%3B10104579731767%3B1409632296065%3B2385390625025; www58com="UserID=71458147739661&UserName=0fxbux8ev"; 58cooper="userid=71458147739661&username=0fxbux8ev"; 58uname=0fxbux8ev; passportAccount="atype=0&bstate=0"; PPU.sig=woHBwOKGVxtCv_ugep6eTec4Vbo; Hm_lpvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1660642704; ppStore_fingerprint=331EA1935B39F35F42D3E8461D1546FBB24A252A5BE5EA8F%EF%BC%BF1660642703564; fzq_js_infodetailweb=b69001bbd84db3b61426cbbbff6f0d93_1660642703592_7; JSESSIONID=1663A4938E2EF1A1DF5C78409B61BD6B; fzq_js_zhaopin_list_pc=d636823dc9ded9aec42ab7aa10a353ff_1660642959798_7; Hm_lpvt_5bcc464efd3454091cf2095d3515ea05=1660642960; PPU=UID=71458147739661&UN=0fxbux8ev&TT=93ecde4f3719cb3dedf5810eefb7a7e9&PBODY=T9Z-NQ8QRAUyo36mcmrtu9Kv4Ij-52fG6f1p1ln1pOW16dvSneVS_xH6AZeZN4dXS2nt2k7qik6G1QHeGQSG55NTq2jbxtbGCT1Kyn5pSRnhZHTghRdojraiuJisbUJRF2GLmTrc--zT9-2Jn_XRLRhIn3Ff2kg__dUEnZljcoI&VER=1&CUID=Ia5GM2c1i47263wLL87x3w',

        }
    }

    def start_requests(self):
        url = 'https://bj.58.com/yingjiangong/pn2/?pid=454607466785308672&PGTID=0d302f81-0000-17be-07d9-5eec830f26fe&ClickID=3'

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
            company_item['name'] = count.xpath('.//*[@class="comp_name"]/a/@title').get()
            company_item['comp_link'] = count.xpath('.//*[@class="comp_name"]/a/@href').get()
            uid = item['link'] + item['job_title']+item['salary']
            item['uid'] = hashlib.md5(uid.encode(encoding='utf-8')).hexdigest()
            # if Redis_DB().redis_job(item['uid']) is True:  # 数据去重
            #     print(item['job_title'], item['link'], '\033[0;35m <=======此岗位已采集=======> \033[0m')
            #     continue
            #print(item['link'],item['education'], item['job_title'], item['work_years'],
            # company_item['name'], item['uid'],company_item['comp_link'])
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
        # 公司item
        company_item = response.meta['company_item']
        # 公司简介
        item['job_desc'] = ''.join(response.xpath('//*[@class="des"]/text()').getall())
        item['city'] = response.xpath('//*[@class="pos_area_item"][1]/text()').get()
        print(item)










