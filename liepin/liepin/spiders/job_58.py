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
from liepin.spiders.ind_city import liepin_ind



class Job58Spider(scrapy.Spider):
    name = 'job_58'
    custom_settings = {
        'COOKIES_ENABLED': False,
        'DEFAULT_REQUEST_HEADERS': {
            'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9', 'cache-control': 'no-cache',
             'cookie': 'userid360_xml=C7977A6730823F910D61E36545E6F68B; time_create=1663225034203; f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; id58=CocHKmJrsvwd00/gBFPwAg==; 58tj_uuid=883f06af-ea1f-4366-8018-3e35725400e7; als=0; wmda_uuid=22af24eb753314591c43d6563191d5af; wmda_new_uuid=1; xxzl_deviceid=wb8gy%2FPMsMYQmw%2BwB5TZAOoxa%2B0WEbhPnxMTVNdk5HUwxd%2BheF7itHNXY97solAH; 58home=bj; myfeet_tooltip=end; xxzl_smartid=610a42d76847430ba91d9f85189542fc; Hm_lvt_fe7700af2f35759e6256aa5635b9c9ff=1659340591; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1659340632; final_history=47907462014755; city=bj; wmda_visited_projects=%3B11187958619315%3B1731916484865%3B2286118353409%3B10104579731767%3B1409632296065%3B2385390625025; __utma=253535702.71241368.1656061471.1661323387.1661326720.7; __utmz=253535702.1661326720.7.7.utmcsr=qy.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/bj_245/; myLat=""; myLon=""; mcity=bj; f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; commontopbar_ipcity=bj%7C%E5%8C%97%E4%BA%AC%7C0; xxzl_cid=82d0de8097ae4b218bb0cf7518483a55; xzuid=580970d0-7108-4f94-84a5-72a409098990; sessionid=072516b5-c9cd-42ef-b87f-c9c389c9e139; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1660644768,1660704526,1661311396,1661393627; Hm_lvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1660289005,1660543846,1661308181,1661393630; fzq_h=5ac02eaef2c163186680c4c5dd8763d0_1661396099938_5a077ec166bc482da1a0f2dc495cd2be_2071877498; www58com="UserID=71458147739661&UserName=0fxbux8ev"; 58cooper="userid=71458147739661&username=0fxbux8ev"; 58uname=0fxbux8ev; passportAccount="atype=0&bstate=0"; wmda_session_id_1731916484865=1661417318377-0eeb0a3f-e9f5-c273; new_uv=26; utm_source=; spm=; init_refer=https%253A%252F%252Fcallback.58.com%252F; wmda_session_id_11187958619315=1661417319688-bd9d9811-348d-954b; new_session=0; PPU.sig=xt9Aw3HVC5_443PHBDthgFaQ_ko; Hm_lpvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1661417373; fzq_js_infodetailweb=6bc776e1d1b833d07dbfa5769f3415b0_1661417373037_9; ppStore_fingerprint=331EA1935B39F35F42D3E8461D1546FBB24A252A5BE5EA8F%EF%BC%BF1661417373082; JSESSIONID=5FCCBFD585F0A57D9067CDC756B24535; fzq_js_zhaopin_list_pc=abcb276604941a2efc71b7964268a57d_1661417413025_7; Hm_lpvt_5bcc464efd3454091cf2095d3515ea05=1661417413; PPU=UID=71458147739661&UN=0fxbux8ev&TT=ed2c17ffbc45e3b974e47ddab003c26e&PBODY=WKWT2YYepn6vxy1zUpDPYVX3oh_8iY_NbNrKhJk11Ow-oJWNTJIUo76RRNp8bSNTvh8-cMIob9a03Dib6oC8jMguhqW9pHrigWIfEVFfbuTGwqmMp-_QoyD2oL1sAHqhRJMufkPofR3Hu-TuG1R6hhJziTvnOFd-lLf5NUTTerQ&VER=1&CUID=Ia5GM2c1i47263wLL87x3w',
             'pragma': 'no-cache', 'referer': 'https://callback.58.com/',
             'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"', 'sec-ch-ua-mobile': '?0',
             'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate',
             'sec-fetch-site': 'same-site', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1',
             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
            }


    def start_requests(self):
        url = 'https://bj.58.com/yingjiangong/pn2/?pid=454607466785308672&PGTID=0d302f81-0000-17be-07d9-5eec830f26fe&ClickID=3'

        yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    # 岗位列表解析
    def parse(self, response, *args, **kwargs):
        count_list = response.xpath('//*[@id="list_con"]/li')
        if count_list is []:
            return
        for count in count_list[0:1]:
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
        yield scrapy.Request(comp_href, callback=self.com_info, meta={'item': copy.deepcopy(item),
                                                                        'company_item': copy.deepcopy(company_item)},
                                                                        dont_filter=True)

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

        cid = company_item['name'] + company_item['comp_code']
        company_item['cid'] = hashlib.md5(cid.encode(encoding='utf-8')).hexdigest()

        item['cid'] = company_item['cid']
        item['comp_name'] = company_item['name']
        print(len(item))
        print(len(company_item))









