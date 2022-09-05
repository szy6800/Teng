# -*- coding: utf-8 -*-

# @Time : 2022-07-23 15:33:49
# @Author : 石张毅
# @Site : https://www.liepin.com/
# @introduce: 猎聘网


import scrapy
import copy
import json
from liepin.items import LiepinJOBItem
from liepin.items import LiepinCompItem
import hashlib
from liepin.tools.DB_redis import Redis_DB
from liepin.spiders.ind_city import liepin_ind


class LpjobSpider(scrapy.Spider):
    name = 'lpjob_js'
    custom_settings = {
        'COOKIES_ENABLED': False,
        'DEFAULT_REQUEST_HEADERS': {
            "Cookie": 'inited_user=83fc4fabea08a638acf3441819698d09; gr_user_id=b21ede8f-e4bd-4638-bf5f-6a6306453010; __uuid=1654585870293.02; __gc_id=f8062ff6c43c443c86e564440b0133a4; need_bind_tel=false; new_user=false; c_flag=762cd6f483231d222d74912fdc67da8d; __s_bid=f255f61873c258e5ccc43dd6a9e8a14be406; imClientId=669dfff6133fba4e7674d3815bdeee65; imId=669dfff6133fba4e91362c0e3c63f8af; imClientId_0=669dfff6133fba4e7674d3815bdeee65; imId_0=669dfff6133fba4e91362c0e3c63f8af; city_site=hz; access_system=C; __tlog=1660787197040.38|00000000|00000000|00000000|00000000; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1660554306,1660701748,1660716854,1660787197; acw_tc=276077d516607871977498965e11d418a38d272aebcd03569439a030a91287; UniqueKey=f8b0ac45bac241ec1a667e00ad0d9493; lt_auth=s7lebiQMnV2q5HiKgGFfta8fjN6hAzrI9HtcgRsF1dfvWvWw4PjrQwqFr7YCxAMhkBJ8dsULN7b+MuD5y3FM60oVwGmklICxv/2k2XgeTuZnHuyflMXuqsjQQ5wtrXg6ykpgn2si; user_roles=0; user_photo=5f8fa3a6f6d1ab58476f322808u.png; user_name=石张毅; inited_user=83fc4fabea08a638acf3441819698d09; imApp_0=1; fe_im_connectJson_0={"0_f8b0ac45bac241ec1a667e00ad0d9493":{"socketConnect":"1","connectDomain":"liepin.com"}}; __session_seq=13; __uv_seq=13; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1660787481; fe_im_opened_pages=_1660787239786_1660787332452_1660787414310_1660787481358; fe_im_socketSequence_new_0=9_9_2',
            "Origin": "https://www.liepin.com",

        }
    }

    def __init__(self, *args, **kwargs):
        super(LpjobSpider, self).__init__()
        # 行业列表
        self.ind = liepin_ind()

    def start_requests(self):
        for i in self.ind[19:20]:
            # 行业链接
            ind_code = i['code']
            # 北京 010  上海020 天津030  重庆040 #广州050020 # 深圳050090 #苏州060080 #南京060020 #杭州070020 #大连210040 #成都280020 #武汉170020 # 西安 270020
            city_code = '270020'
            job_indu = i['small_type']
            for i in range(0,10):
                data = {"data":{"mainSearchPcConditionForm":{"city":city_code,"dq":city_code,"pubTime":"","currentPage":f'{i}',"pageSize":'40',"key":"","workYearCode":"0","compId":"","compName":"","compTag":"","industry":f"10${ind_code}","salary":"","jobKind":"","compScale":"","compKind":"","compStage":"","eduLevel":""},"passThroughForm":{"ckId":"djeop3vgn5cdv8b26z839jw4o5ze6hqa","scene":"page","skId":"kccoiw63x88gfq7kaybm12mufpmkkn1b",                                                                                                                                                                                                                                                                                                               "fkId":"ahsgpbkabqodk63sr7tbs2ap2o0ur068","sfrom":"search_job_pc"}}}
                url = 'https://apic.liepin.com/api/com.liepin.searchfront4c.pc-search-job'
                yield scrapy.FormRequest(
                    url=url,
                    method='POST',
                    body=json.dumps(data),
                    headers={'Content-Type': 'application/json'},
                    callback=self.parse,
                    dont_filter=True,
                    meta={'job_indu':job_indu})

    def parse(self, response, *args, **kwargs):
        json_text = json.loads(response.text)
        count_list = json_text['data']['data']['jobCardList']
        for count in count_list:
            item = LiepinJOBItem()
            item['link'] = count['job']['link']+'?'
            # 网站来源
            item['source'] = '猎聘网'
            # 备用字段
            item['base'] = ''
            # 发布时间
            item['pub_time'] = ''
            # 岗位名称
            item['job_title'] = count['job']['title']
            # 薪资
            item['salary'] = count['job']['salary']
            # 工作种类
            item['job_indu'] = response.meta['job_indu']
            # 公司信息
            company_item = LiepinCompItem()
            # 公司行业
            company_item['comp_ind'] = count['comp']['compIndustry']
            # 融资阶段
            try:
                company_item['fig_stage'] = count['comp']['compStage']
            except:
                company_item['fig_stage'] = ''
            # 人数规模
            try:
                company_item['num_of_peo'] = count['comp']['compScale']
            except:
                company_item['num_of_peo'] = ''
            # 公司logo
            logo = count['comp']['compLogo']
            company_item['logo'] = f'https://image0.lietou-static.com/bg_white_80x80/{logo}'
            # 公司列表名
            name = count['comp']['compName']
            uid = item['link'] + item['job_title'] + name +item['salary']
            # 岗位去重
            item['uid'] = hashlib.md5(uid.encode(encoding='utf-8')).hexdigest()
            # print(company_item)
            if Redis_DB().redis_job(item['uid']) is True:  # 数据去重
                print(item['job_title'],item['link'], '\033[0;35m <=======此岗位已采集=======> \033[0m')
                continue
            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item),
                                                     'company_item': copy.deepcopy(company_item)},
                                 dont_filter=True)


    def parse_info(self, response):
        # print(response.text)
        if response.status != 200:
            return
        item = response.meta['item']
        # 公司item
        company_item = response.meta['company_item']
        # 岗位描述
        item['job_desc'] = response.xpath('//*[@data-selector="job-intro-content"]/text()').get()
        # 所在城市
        item['city'] = response.xpath('//*[@class="job-properties"]/span[1]/text()').get()
        # 工作年限
        item['work_years'] = response.xpath('//*[@class="job-properties"]/span[3]/text()').get()
        # 学历要求
        item['education'] = response.xpath('//*[@class="job-properties"]/span[5]/text()').get()
        # 标签
        item['job_tags'] = '|'.join(response.xpath('//*[@class="tag-box"]/ul/li/text()').getall())
        item['comp_name'] = response.xpath('//*[@class="company-info-container"]//div[@class="name ellipsis-1"]/text()').get()
        if item['comp_name'] is None:
            comp_name = response.xpath('//*[@class="title-box"]/span[2]/text()').getall()
            if len(comp_name) == 2:
                item['comp_name'] = response.xpath('//*[@class="title-box"]/span[2]/div/text()').get()
            else:
                item['comp_name'] = response.xpath('//*[@class="title-box"]/span[2]/text()').get().strip().replace('· ','')
        # 公司名
        # company_item['name'] = item['comp_name']
        company_item['link'] = response.url
        lng = response.xpath('//*[@id="location"]/@value').get()
        try:
            company_item['lng'] = lng.split(',')[0]
            company_item['lat'] = lng.split(',')[1]
        except:
            company_item['lng'] = ''
            company_item['lat'] = ''
        # 公司官网
        company_item['comp_website'] = ''
        company_item['comp_addr'] = response.xpath("//*[contains(text(),'职位地址：')]/following::span[1]/text()").get()
        # 注册时间
        company_item['reg_time'] = response.xpath("//*[contains(text(),'注册时间：')]/following::span[1]/text()").get()
        # 注册资本
        company_item['reg_capi'] = response.xpath("//*[contains(text(),'注册资本：')]/following::span[1]/text()").get()
        # 经营期限
        company_item['op_period'] = response.xpath("//*[contains(text(),'经营期限：')]/following::span[1]/text()").get()
        # 经营范围
        company_item['man_range'] = response.xpath("//*[contains(text(),'经营范围：')]/following::span[1]/text()").get()
        # 公司简介
        comp_desc = response.xpath('//*[@class="company-intro-container"]//div[contains(@class,"inner")]/text()').get()
        if comp_desc is None:
            company_item['comp_desc'] = ''
        else:
            company_item['comp_desc'] = comp_desc
        company_item['welfare'] = '|'.join(response.xpath('//*[@class="job-apply-container-left"]/div[1]/span/text()').getall())
        # 公司详情链接
        company_item['comp_link'] = response.xpath('//*[@class="title-box"]//a[contains(@href,"com/company/")]/@href').get()
        if company_item['comp_link'] is None:
            company_item['name'] = item['comp_name']
            company_item['comp_code'] = ''
            company_item['reg_au'] = ''
            company_item['legal_peo'] = ''
            company_item['status'] = ''
            company_item['locations'] = ''
            company_item['comp_type'] = ''
            cid = item['comp_name'] + company_item['comp_ind']
            company_item['cid'] = hashlib.md5(cid.encode(encoding='utf-8')).hexdigest()
            item['cid'] = company_item['cid']
            # print(company_item)
            yield company_item
            yield item
        else:
            yield scrapy.Request(company_item['comp_link'], callback=self.com_info, meta={'item': copy.deepcopy(item),'company_item': copy.deepcopy(company_item)},
                                 dont_filter=True)

    # 公司详情
    def com_info(self, response):
        # print(response.text)
        if response.status != 200:
            return
        company_item = response.meta['company_item']
        item = response.meta['item']
        # 公司名
        company_item['name'] = response.xpath("//*[contains(text(),'企业全称')]/following::p[1]/text()").get()
        if company_item['name'] is None:
            company_item['name'] = item['comp_name']
        company_item['comp_code'] = response.xpath("//*[contains(text(),'统一信用代码')]/following::p[1]/text()").get()
        company_item['reg_au'] = response.xpath("//*[contains(text(),'登记机关')]/following::p[1]/text()").get()
        company_item['legal_peo'] = response.xpath("//*[contains(text(),'法人代表')]/following::p[1]/text()").get()
        company_item['status'] = response.xpath("//*[contains(text(),'经营状态')]/following::p[1]/text()").get()
        company_item['locations'] = response.xpath("//*[contains(text(),'所在地')]/following::p[1]/text()").get()
        company_item['comp_type'] = response.xpath("//*[contains(text(),'企业类型')]/following::p[1]/text()").get()
        cid = item['comp_name'] + company_item['comp_ind']
        company_item['cid'] = hashlib.md5(cid.encode(encoding='utf-8')).hexdigest()
        item['cid'] = company_item['cid']
        # print(company_item)
        yield item
        yield company_item


