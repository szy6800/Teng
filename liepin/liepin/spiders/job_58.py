# -*- coding: utf-8 -*-

# @Time : 2022-08-01 13:53:45
# @Author : 石张毅
# @Site : https://bj.58.com/tech/?key=%E6%8B%9B%E8%81%98&cmcskey=%E6%8B%9B%E8%81%98&final=1&jump=1&specialtype=gls&classpolicy=uuid_5b53e4813aca4a90b528600379ab5e1e,displocalid_1,from_main,to_jump,tradeline_job,classify_D&PGTID=0d302408-0000-1ff5-f3d6-2c565a6ca769&ClickID=3
# @introduce: 58同城招聘

import scrapy


class Job58Spider(scrapy.Spider):
    name = 'job_58'
    # custom_settings = {
    #     'COOKIES_ENABLED': False,
    #     'DEFAULT_REQUEST_HEADERS': {
    #         "Cookie": 'f=n; commontopbar_new_city_info=1|北京|bj; f=n; commontopbar_new_city_info=1|北京|bj; time_create=1661925581178; userid360_xml=C7977A6730823F910D61E36545E6F68B; id58=CocHKmJrsvwd00/gBFPwAg==; 58tj_uuid=883f06af-ea1f-4366-8018-3e35725400e7; als=0; wmda_uuid=22af24eb753314591c43d6563191d5af; wmda_new_uuid=1; xxzl_deviceid=wb8gy/PMsMYQmw+wB5TZAOoxa+0WEbhPnxMTVNdk5HUwxd+heF7itHNXY97solAH; wmda_visited_projects=;11187958619315;1731916484865;2286118353409;10104579731767; 58home=bj; f=n; commontopbar_new_city_info=1|北京|bj; commontopbar_ipcity=bj|北京|0; city=bj; sessionid=3cda78c2-5f56-4765-a1d9-acb460e821e7; fzq_h=78797577584cb36b3120b130977c468f_1659325897419_9316fa20d68c4432933f14aa927d4e64_2071877498; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1659325898; Hm_lvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1659326041; __utmc=253535702; myfeet_tooltip=end; spm=; utm_source=; new_uv=4; new_session=0; wmda_session_id_1731916484865=1659331813258-68a4d3af-bb15-c33f; wmda_session_id_11187958619315=1659331843332-9c852241-6e56-c800; __utmz=253535702.1659331880.3.3.utmcsr=qy.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/73533032889614/; __utma=253535702.71241368.1656061471.1659326049.1659331880.3; init_refer=http%3A%2F%2Flocalhost%3A63342%2F; xxzl_cid=82d0de8097ae4b218bb0cf7518483a55; xzuid=580970d0-7108-4f94-84a5-72a409098990; fzq_js_infodetailweb=f4a4b2cddf9725070a256913b8b20d8b_1659335959524_7; Hm_lpvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1659335960; ppStore_fingerprint=331EA1935B39F35F42D3E8461D1546FBB24A252A5BE5EA8F＿1659335959617; www58com="UserID=71458147739661&UserName=0fxbux8ev"; 58cooper="userid=71458147739661&username=0fxbux8ev"; 58uname=0fxbux8ev; passportAccount="atype=0&bstate=0"; PPU=UID=71458147739661&UN=0fxbux8ev&TT=0cc2c706277151dee90c649842ab5cb0&PBODY=gonqSriUJGFM9mFIqkF9L1k5zLBDx02dwNhntr0v0yWUlfiuFc2Veg4FOF-PjnYgmMeEox3_vR0OKZRAaWkdx7Kbu8Ks2BqsdHQgChs1NU4bsXe3AVoIF2EWksduWGx3K_o6EiE4Gn2Ygd2ffzR4LTaLG2RKcLitkYlWGcWFOh8&VER=1&CUID=Ia5GM2c1i47263wLL87x3w; crmvip=; dk_cookie=; xxzl_smartid=610a42d76847430ba91d9f85189542fc; JSESSIONID=55C524B48B6AC0F25E07586A4BD3C024; fzq_js_zhaopin_list_pc=880e2ae82027bfaaf5a007f86fc8cb27_1659337761334_9; Hm_lpvt_5bcc464efd3454091cf2095d3515ea05=1659337762'
    #     }
    # }

    def start_requests(self):
        url = 'https://bj.58.com/tech/pn13/?key=%E6%8B%9B%E8%81%98&cmcskey=%E6%8B%9B%E8%81%98&final=1&jump=1&specialtype=gls&classpolicy=uuid_5b53e4813aca4a90b528600379ab5e1e,displocalid_1,from_main,to_jump,tradeline_job,classify_D&pid=452840702995169280&PGTID=0d303655-0000-1949-edf8-aa10337b21bd&ClickID=3'
        yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response, *args, **kwargs):
        # print(response.text)
        res = response.xpath('//*[@class="item_con apply"]/@infoid').getall()
        print(res)

