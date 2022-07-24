
import scrapy
import json
import jsonpath
import copy
from liepin.items import LiepinJOBItem
from liepin.items import LiepinCompItem
import hashlib

class LpjobSpider(scrapy.Spider):
    name = 'lpjob'

    def __init__(self, *args, **kwargs):
        super(LpjobSpider, self).__init__()

        # self.result = dbz()
    def start_requests(self):

        url = 'https://www.liepin.com/zhaopin/?headId=9296d84423d70bfb31a63874d29dce6e&ckId=qjifw5vzwgtepwq3dle9hx6a4wvense8&oldCkId=9abde3568e7bf67336a7b9168605ba7d&fkId=fer793ehy1njp3co234146pvyjnats88&skId=1xr9gptsswpl8wpfizgd4ly6bfrau1a9&sfrom=search_job_pc&industry=1$040&dq=010&currentPage=1&scene=page'
        yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response, *args, **kwargs):
        count_list = response.xpath('//*[@class="left-list-box"]/ul/li')
        if count_list is []:
            return
        for count in count_list:
            item = LiepinJOBItem()
            item['link'] = count.xpath('.//*[@data-nick="job-detail-job-info"]/@href').get()
            # 岗位名称
            item['job_title'] = count.xpath('.//*[@class="job-title-box"]/div/@title').get()
            # # 公司地址
            # item['job_addr'] = count.xpath('.//*[@class="job-dq-box"]/span[@class="ellipsis-1"]/text()').get()
            # 薪资
            item['salary'] = count.xpath('.//*[@class="job-salary"]/text()').get()
            # 工作种类
            item['job_indu'] = ''

            yield scrapy.Request(item['link'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        # print(response.text)
        if response.status != 200:
            return
        item = response.meta['item']
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
        # 公司名
        item['comp_name'] = response.xpath('//*[@class="company-info-container"]//div[@class="name ellipsis-1"]/text()').get()
        if item['comp_name'] is None:
            item['comp_name'] = response.xpath('//*[@class="title-box"]/span[2]/text()|//*[@class="title-box"]/span[2]/div/text()').get().strip().replace('· ','')
        # 公司表
        uid = item['link'] + item['job_title']+item['job_desc']+item['comp_name']
        item['uid'] = hashlib.md5(uid.encode(encoding='utf-8')).hexdigest()

        company_item = LiepinCompItem()
        company_item['name'] = item['comp_name']
        company_item['link'] = response.url
        # 公司行业
        company_item['comp_ind'] = response.xpath("//*[contains(text(),'企业行业：')]/following::span[1]/text()").get()
        # 人数规模
        lng = response.xpath('//*[@id="location"]/@value').get()
        try:
            company_item['lng'] = lng.split(',')[0]
            company_item['lat'] = lng.split(',')[1]
        except:
            company_item['lng'] = ''
            company_item['lat'] = ''
        company_item['num_of_peo'] = response.xpath("//*[contains(text(),'人数规模：')]/following::span[1]/text()").get()
        # 融资阶段
        company_item['fig_stage'] = response.xpath("//*[contains(text(),'融资阶段：')]/following::span[1]/text()").get()
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
        # 经纬度
        company_item['cid'] = ''
        yield company_item
        yield item
