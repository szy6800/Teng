# -*- coding: utf-8 -*-

# @Author : 石张毅
# @Site : http://139.170.150.135/dataservice/query/project/list
# @introduce:
import copy
import hashlib
import scrapy
import re


class SchoolSpider(scrapy.Spider):
    name = 'school'
    # allowed_domains = ['139.170.150.135']
    # start_urls = ['http://139.170.150.135/']

    def start_requests(self):
        for i in range(600,622):
            url = "http://139.170.150.135/dataservice/query/project/list"
            formdata = {
                "$total":"9262",
                "$reload":"0",
                "$pg":"{}".format(i),
                "$pgsz":"15",
            }
            yield scrapy.FormRequest(url=url, formdata=formdata, callback=self.parse)

    def parse(self, response, **kwargs):
        # 列表页链接
        list_url = response.xpath('//*[@class="table_box"]//tr/@onclick').getall()
        for href in list_url:
            item = dict()
            item['url'] = response.urljoin(re.findall("href='(.*?)'", href)[0])
            yield scrapy.Request(item['url'], callback=self.parse_info, meta={'item': copy.deepcopy(item)},
                                 dont_filter=True)

    def parse_info(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 项目编号
        item['num'] = response.xpath("//span[contains(text(),'项目编号：')]/following::text()[1]").get()
        # 项目名字
        item['name'] = response.xpath('//*[@class="user_info tip"]/@title').get()
        # 项目分类
        item['type'] = response.xpath("//span[contains(text(),'项目分类：')]/following::text()[1]").get()
        # 建设单位
        item['builder'] = response.xpath("//span[contains(text(),'建设单位：')]/following::text()[1]").get()
        # 所属区域
        item['address'] = response.xpath("//span[contains(text(),'所在区划：')]/following::text()[1]").get()
        # 建设地址
        item['bui_add'] = response.xpath("//span[contains(text(),'建设地址：')]/following::text()[1]").get()
        # 负责人
        item['leader'] = response.xpath("//span[contains(text(),'项目负责人：')]/following::text()[1]").get()
        # 项目用途
        item['purpose'] = response.xpath("//span[contains(text(),'项目用途：')]/following::text()[1]").get()
        # 建设性质
        item['bui_nature'] = response.xpath("//span[contains(text(),'建设性质：')]/following::text()[1]").get()
        # 项目规模
        item['scale'] = response.xpath("//span[contains(text(),'项目规模：')]/following::text()[1]").get()
        # 建档时间
        item['filing_time'] = response.xpath("//span[contains(text(),'建档时间：')]/following::text()[1]").get().replace('年', '-')\
            .replace('月', '-').replace('日', '')
        # 机构代码
        item['code'] = response.xpath("//span[contains(text(),'机构代码：')]/following::text()[1]").get()
        # 资金性质
        item['fu_nature'] = response.xpath("//span[contains(text(),'资金性质：')]/following::text()[1]").get()
        # 建设模式
        item['bui_mode'] = response.xpath("//span[contains(text(),'建设模式：')]/following::text()[1]").get()
        # 建筑面积（长度）
        item['bui_area'] = response.xpath("//span[contains(text(),'建筑面积（长度）：')]/following::text()[1]").get()
        # 立项文号
        item['doc_num'] = response.xpath("//span[contains(text(),'立项文号：')]/following::text()[1]").get().strip()
        # 立项级别
        item['doc_level'] = response.xpath("//span[contains(text(),'立项级别：')]/following::text()[1]").get().strip()
        # 批复机关
        item['check_unit'] = response.xpath("//span[contains(text(),'批复机关：')]/following::text()[1]").get().strip()
        # 批复时间
        item['check_time'] = response.xpath("//span[contains(text(),'批复时间：')]/following::text()[1]").get().strip().replace('年', '-')\
            .replace('月', '-').replace('日', '')
        # 建设用地规划许可证
        item['land_licence'] = response.xpath("//span[contains(text(),'建设用地规划许可证：')]/following::text()[1]").get().strip()
        #  建设工程规划许可证
        item['eng_licence'] = response.xpath("//span[contains(text(),'建设工程规划许可证：')]/following::text()[1]").get().strip()
        # 预算总投资
        item['total_inv'] = response.xpath("//span[contains(text(),'预算总投资：')]/following::text()[1]").get()
        # 其他资金
        item['other_inv'] = response.xpath("//span[contains(text(),'预算总投资：')]/following::dd[1]/text()").get()
        # 建设内容说明
        item['bui_dec'] = response.xpath("//span[contains(text(),'建设内容说明：')]/following::text()[1]").get().strip()
        # 建设内容简介
        item['bui_acc'] = response.xpath("//span[contains(text(),'建设项目简介：')]/following::text()[1]").get().strip()
        unit_url = response.xpath("//a[@data-contentid='iframe_tab']/@data-url").get()

        yield scrapy.Request(response.urljoin(unit_url), callback=self.parse_unit, meta={'item': copy.deepcopy(item)},
                             dont_filter=True)

    def parse_unit(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 单位工程编码
        item['unit_pro_num'] = '|'.join(response.xpath("//*[contains(text(),'建筑')]/preceding::tr[1]/td[2]/text()").getall())
        # 单位工程名称
        item['unit_pro_name'] = '|'.join(response.xpath("//*[contains(text(),'建筑')]/preceding::tr[1]/td[3]/text()").getall())
        # 工程专业类别
        item['unit_pro_type'] = '|'.join(response.xpath("//*[contains(text(),'建筑')]/preceding::tr[1]/td[4]/text()").getall())
        # 建筑
        item['unit_pro_bui'] = '|'.join(response.xpath("//*[contains(text(),'建筑')]/following::td[1]/text()").getall())
        # 结构
        item['unit_pro_str'] = '|'.join(response.xpath("//*[contains(text(),'结构')]/following::td[1]/text()").getall())
        # 勘察
        item['unit_pro_che'] = '|'.join(response.xpath("//*[contains(text(),'勘察')]/following::td[1]/text()").getall())
        url = response.url
        map_url = url.replace('projDwgcList', 'toProjMap')
        yield scrapy.Request(response.urljoin(map_url), callback=self.parse_map, meta={'item': copy.deepcopy(item)},
                             dont_filter=True)

    # 解析地图表中经纬度
    def parse_map(self, response):
        if response.status != 200:
            return
        item = response.meta['item']
        # 单位工程编码
        item['lng'] = re.search("lng='(.*?)';", response.text).group(1)
        item['lat'] = re.search("lat='(.*?)';", response.text).group(1)
        check_md5 = item['url']+item['name']
        item['check_md5'] = hashlib.md5(check_md5.encode(encoding='utf-8')).hexdigest()
        yield item













