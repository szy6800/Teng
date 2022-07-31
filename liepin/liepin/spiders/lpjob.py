# -*- coding: utf-8 -*-

# @Time : 2022-07-23 15:33:49
# @Author : 石张毅
# @Site :
# @introduce: 猎聘网


import re
import scrapy
import copy
from liepin.items import LiepinJOBItem
from liepin.items import LiepinCompItem
import hashlib
from liepin.tools.DB_redis import Redis_DB


class LpjobSpider(scrapy.Spider):
    name = 'lpjob'

    def __init__(self, *args, **kwargs):
        super(LpjobSpider, self).__init__()
        self.ind = ''

        # self.result = dbz()
    def start_requests(self):

        url = 'https://www.liepin.com/zhaopin/?headId=02c89b9548d8aea7d7a2046b464d68c6&ckId=mldrhthumlud7kfrj3bx1d5ibx91l3u8&oldCkId=2c62fc66a9ddb29d80a521c6946831c8&fkId=14b3fo4tosqmflesgfhuvrkhpchl5jn9&skId=go4ep8zdmmwrpyvywy59ur28rqx685p8&sfrom=search_job_pc&industry=10$280&dq=040&currentPage=2&scene=page'
        yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response, *args, **kwargs):
        count_list = response.xpath('//*[@class="left-list-box"]/ul/li')
        if count_list is []:
            return
        for count in count_list:
            item = LiepinJOBItem()
            link = count.xpath('.//*[@data-nick="job-detail-job-info"]/@href').get()
            # print(link)
            item['link'] = re.findall('https://www.liepin.com/.*?\?', link)[0]
            # 网站来源
            item['source'] = '猎聘网'
            # 备用字段
            item['base'] = ''
            # print(len(item['link']))
            # print(item['link'])
            # 岗位名称
            item['job_title'] = count.xpath('.//*[@class="job-title-box"]/div/@title').get()
            # # 公司地址
            # item['job_addr'] = count.xpath('.//*[@class="job-dq-box"]/span[@class="ellipsis-1"]/text()').get()
            # 薪资
            item['salary'] = count.xpath('.//*[@class="job-salary"]/text()').get()
            # 工作种类
            item['job_indu'] = ''

            # 公司信息
            company_item = LiepinCompItem()
            jo1 = count.xpath('.//*[@class="company-tags-box ellipsis-1"]/span').getall()
            if len(jo1) == 3:
                # 公司行业
                company_item['comp_ind'] = re.findall('<span>(.*?)</span>', jo1[0])[0]
                # 融资阶段
                company_item['fig_stage'] = re.findall('<span>(.*?)</span>', jo1[1])[0]
                # 人数规模
                company_item['num_of_peo'] = re.findall('<span>(.*?)</span>', jo1[2])[0]
            elif len(jo1) == 2:
                company_item['comp_ind'] = re.findall('<span>(.*?)</span>', jo1[0])[0]
                peo = re.findall('<span>(.*?)</span>', jo1[1])[0]
                if '人' in peo:
                    company_item['num_of_peo'] =peo
                    company_item['fig_stage'] = ''
                else:
                    company_item['num_of_peo'] = ''
                    company_item['fig_stage'] = peo
            elif len(jo1) == 1:
                company_item['comp_ind'] = re.findall('<span>(.*?)</span>', jo1[0])[0]
                company_item['fig_stage'] = ''
                company_item['num_of_peo'] = ''
            # 公司logo
            company_item['logo'] = response.urljoin(count.xpath('.//*[@class="company-logo"]/img/@src').get())
            # 公司列表名
            name = count.xpath('.//*[@class="company-logo"]/img/@alt').get()
            uid = item['link'] + item['job_title'] + name +item['salary']
            # 岗位去重
            item['uid'] = hashlib.md5(uid.encode(encoding='utf-8')).hexdigest()
            if Redis_DB().redis_job(item['uid']) is True:  # 数据去重
                print(item['job_title'], '\033[0;35m <=======此岗位已采集=======> \033[0m')
                continue
            # 公司去重
            # cid = name + company_item['comp_ind']
            # company_item['cid'] = hashlib.md5(cid.encode(encoding='utf-8')).hexdigest()
            # if Redis_DB().redis_comp(company_item['cid']) is True:  # 数据去重
            #     print(company_item['name'], '\033[0;35m <=======此公司已采集=======> \033[0m')
            #     return
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
            item['comp_name'] = response.xpath('//*[@class="title-box"]/span[2]/text()|//*[@class="title-box"]/span[2]/div/text()').get().strip().replace('· ','')
        # 公司信息
        # 公司名
        company_item['name'] = item['comp_name']
        company_item['link'] = response.url
        # 公司行业
        #company_item['comp_ind'] = response.xpath("//*[contains(text(),'企业行业：')]/following::span[1]/text()").get()
        # 人数规模
        lng = response.xpath('//*[@id="location"]/@value').get()
        try:
            company_item['lng'] = lng.split(',')[0]
            company_item['lat'] = lng.split(',')[1]
        except:
            company_item['lng'] = ''
            company_item['lat'] = ''
        #company_item['num_of_peo'] = response.xpath("//*[contains(text(),'人数规模：')]/following::span[1]/text()").get()
        # 融资阶段
        #company_item['fig_stage'] = response.xpath("//*[contains(text(),'融资阶段：')]/following::span[1]/text()").get()
        # 公司地址
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
        company_item['comp_desc'] = response.xpath('//*[@class="company-intro-container"]//div[contains(@class,"inner")]/text()').get()

        company_item['welfare'] = '|'.join(response.xpath('//*[@class="job-apply-container-left"]/div[1]/span/text()').getall())
        # 岗位id和公司id
        cid = company_item['name'] + company_item['comp_ind']
        company_item['cid'] = hashlib.md5(cid.encode(encoding='utf-8')).hexdigest()
        item['cid'] = company_item['cid']
        yield company_item

        yield item
