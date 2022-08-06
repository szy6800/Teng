# -*- coding: utf-8 -*-

# @Time : 2022-08-01 13:53:45
# @Author : 石张毅
# @Site : https://bj.58.com/
# @introduce: 58同城招聘

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
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh,en;q=0.9,zh-CN;q=0.8,vi;q=0.7,ko;q=0.6',
            'cookie': 'f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; userid360_xml=003B0B7DD9EA28E62916BCB409FCEEEF; time_create=1662346058414; id58=CocG42IZ/xy9/7mLErkOAg==; 58tj_uuid=99e71191-9e21-4654-b203-8c924c2cea9c; als=0; wmda_uuid=93c07d553a63dc9df0e5bcda6f229015; Hm_lvt_3013163ef40dcfa5b06ea83e8a1a797f=1645870881; Hm_lvt_fe7700af2f35759e6256aa5635b9c9ff=1645870881; gr_user_id=35f72dff-1ce3-4dae-9061-07f4b5e5594e; xxzl_deviceid=v9UYVKqMKX%2BgUwFigjqyE0I2rAO5tk1mIvcAx9JuSzSI6L%2FGxZz%2BGkIgWCWGI%2Bub; __utma=253535702.1408907173.1645870892.1645870892.1645870892.1; __utmz=253535702.1645870892.1.1.utmcsr=bj.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/; Hm_lvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1645870965; ppStore_fingerprint=22471D9B27FCED76F9F16C313BDB2F4DCBCDE535D1900109%EF%BC%BF1645870976569; sessionid=500a7d44-5326-4893-94f9-9993fe682bb6; fzq_h=4cf0d3aa05e22704746acbc605fbab5a_1659753338724_e3ff8e094d7446fd820b012de3ac411b_1874969889; wmda_session_id_1731916484865=1659753339288-6b70fb49-4d59-777a; spm=; utm_source=; new_uv=2; init_refer=https%253A%252F%252Fcallback.58.com%252F; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1659753340; 58home=bj; f=n; wmda_session_id_11187958619315=1659753340939-d46e4b82-2844-5e8f; www58com="UserID=71458147739661&UserName=0fxbux8ev"; 58cooper="userid=71458147739661&username=0fxbux8ev"; 58uname=0fxbux8ev; passportAccount="atype=0&bstate=0"; new_session=0; xxzl_smartid=193b68c9992ad8b78999ed9b53f74b7d; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; city=bj; commontopbar_ipcity=bj%7C%E5%8C%97%E4%BA%AC%7C0; wmda_session_id_1409632296065=1659753732206-328f8288-2a6d-94a6; wmda_visited_projects=%3B11187958619315%3B1731916484865%3B1409632296065; Hm_lvt_ad024d0e0914a20e88ae3423b878a182=1659753733; Hm_lpvt_ad024d0e0914a20e88ae3423b878a182=1659753733; PPU.sig=cEYvV79eKqUTjHmvqHrlOAu_Zuk; xzfzqtoken=dPgCSVq3%2BZPEzpgBUciOhspWXnnmozbkqxrVOpR0dB%2FYRabZn1aAx3hWrQKIdZsnin35brBb%2F%2FeSODvMgkQULA%3D%3D; xxzl_cid=53e07ae5dadb4c80ad22a4f7e6ae5fdb; xzuid=b3031ea2-a74f-473b-aa0c-c2b45d0562ac; JSESSIONID=67C25EC5BB2491EF6FFB00C1205F22AB; fzq_js_zhaopin_list_pc=6ec9a6ee7a6d8274d3f71c114d44022c_1659754294058_6; Hm_lpvt_5bcc464efd3454091cf2095d3515ea05=1659754294; PPU="UID=71458147739661&UN=0fxbux8ev&TT=887a3ce1362562f6c7ae2b40f9a1733f&PBODY=U5Dj1gDiA_hVj2mcQpJctkdrCBqOZc57wnpLDZfxRylgfjAgzDAghYMh2__vEUO7d2HyV8ydNlCzq_x_dvIrx0Mjcuv4rZdg445-i2ZswPUeyiuUmKZ1fUqlTB08_BDN3qvygjw09uDy_EGa7wcxNX9IhdTFRRreVOoF43KGKoQ&VER=1&CUID=Ia5GM2c1i47263wLL87x3w"',
            'referer': 'https://bj.58.com/jishuzhichi/pn3/?pid=454597533263659009&PGTID=0d302f85-0000-13ac-0715-fc008e730a13&ClickID=3',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        }
    }

    def start_requests(self):
        url = 'https://bj.58.com/yingjiangong/pn2/?pid=454607466785308672&PGTID=0d302f81-0000-17be-07d9-5eec830f26fe&ClickID=3'
        yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response, *args, **kwargs):
        count_list = response.xpath('//*[@id="list_con"]/li')
        if count_list is []:
            return
        for count in count_list[0:1]:
            item = LiepinJOBItem()
            link_id = count.xpath('.//*[@class="item_con apply"]/@infoid').get()
            link = f'https://bj.58.com/tech/{link_id}x.shtml?'
            print(link)
            yield scrapy.Request(link,callback=self.parse_info)

    def parse_info(self,response):
        # pass
        print(response.text)








