# -*- coding: utf-8 -*-

# @Time : 2022-07-23 15:33:49
# @Author : 石张毅
# @Site :
# @introduce: 猎聘网


import re
import scrapy


class LpjobSpider(scrapy.Spider):
    name = 'lpjob'
    custom_settings = {
        'COOKIES_ENABLED': False,
        'DEFAULT_REQUEST_HEADERS': {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9', 'cache-control': 'no-cache', 'cookie': 'f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; SECKEY_ABVK=DUgxuaSXTX2L4Xn0jnvs8zJYxr8CTuY5+7EqzQNQUEo%3D; BMAP_SECKEY=wkT-bogpsnQn7FNJ1tIvLeWYG2rskJnHTY63Sk5gOYyc5T73kXHlax8o8fePZiDb0WiyLDxfTIAd6u0tKxCVmIBM_fokurrf5FWohX5TCV0A9PTMoFyM9gjuqW9BbotoEf1I3juhCzfzThnEGpEbgJxf5MVx0b-eZK9cU-MKhaSv0u80E7oH3S1K_BOF8Y94; id58=CocHKmJrsvwd00/gBFPwAg==; 58tj_uuid=883f06af-ea1f-4366-8018-3e35725400e7; als=0; wmda_uuid=22af24eb753314591c43d6563191d5af; wmda_new_uuid=1; xxzl_deviceid=wb8gy%2FPMsMYQmw%2BwB5TZAOoxa%2B0WEbhPnxMTVNdk5HUwxd%2BheF7itHNXY97solAH; 58home=bj; myfeet_tooltip=end; xxzl_smartid=610a42d76847430ba91d9f85189542fc; Hm_lvt_fe7700af2f35759e6256aa5635b9c9ff=1659340591; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1659340632; final_history=47907462014755; city=bj; wmda_visited_projects=%3B11187958619315%3B1731916484865%3B2286118353409%3B10104579731767%3B1409632296065%3B2385390625025; myLat=""; myLon=""; mcity=bj; f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; commontopbar_ipcity=bj%7C%E5%8C%97%E4%BA%AC%7C0; xxzl_cid=82d0de8097ae4b218bb0cf7518483a55; xzuid=580970d0-7108-4f94-84a5-72a409098990; sessionid=002ceda5-e77c-4d4f-83bf-e6604ee99699; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1660704526,1661311396,1661393627,1661479829; Hm_lvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1660543846,1661308181,1661393630,1661479831; __utmc=253535702; www58com="UserID=71458147739661&UserName=0fxbux8ev"; 58cooper="userid=71458147739661&username=0fxbux8ev"; 58uname=0fxbux8ev; passportAccount="atype=0&bstate=0"; bangtoptipclose=1; fzq_h=11aa77573a013950786b222bf2b08994_1661484250437_9e2c2538d97e44b9a89afaa1ee5e06dd_2071877498; PPU.sig=LjT329URbPaHLagc5KDC8EfQRkw; JSESSIONID=299FCE00A779CD3846F17063A3195AD0; fzq_js_zhaopin_list_pc=a06dd1edb826e81426a24c07e3d3bd66_1661484784912_9; Hm_lpvt_5bcc464efd3454091cf2095d3515ea05=1661484785; wmda_session_id_1731916484865=1661490840050-676c4200-46fd-1486; new_uv=29; utm_source=; spm=; init_refer=; new_session=0; __utma=253535702.71241368.1656061471.1661484410.1661490867.10; __utmz=253535702.1661490867.10.9.utmcsr=qy.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/85346804754699/; wmda_session_id_2286118353409=1661492650932-dcc2f839-4e82-022b; wmda_session_id_11187958619315=1661492759346-1fcc522f-d54d-191c; __utmt_pageTracker=1; __utmb=253535702.10.10.1661490867; Hm_lpvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1661493659; fzq_js_infodetailweb=177e297906edc72cb4039f805a51a331_1661493659316_7; ppStore_fingerprint=331EA1935B39F35F42D3E8461D1546FBB24A252A5BE5EA8F%EF%BC%BF1661493660735; PPU="UID=71458147739661&UN=0fxbux8ev&TT=0372ec3ab659f2d0601bdc6b670fa7a3&PBODY=VtmQP0mT28yy6_kEUbo3ULV7fCfaoBUNz8y6LpswtURtpy6cnX9T9C-7W4OtOTCkvNdkhCfzHovCvOkfb1Pq5W4GKzyEKdW_1LhkVBQ41fgv3YFsKjt5RP5S7lw6m5WYb6pttC7XxyrlLjVYrkM1h2AqjaTLKgFL_CCmCjcb6OA&VER=1&CUID=Ia5GM2c1i47263wLL87x3w"', 'pragma': 'no-cache', 'referer': 'https://callback.58.com/', 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'same-site', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

    }


    def __init__(self, *args, **kwargs):
        super(LpjobSpider, self).__init__()
        self.ind = ''

        # self.result = dbz()
    def start_requests(self):

        url = 'https://bj.58.com/yewu/?PGTID=0d302551-0000-14e4-c8fb-818d57db6ea4&ClickID=1'
        yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response, *args, **kwargs):
        count_list = response.xpath('//*[@id="filterTrade"]/ul/li[position()>1]')
        if count_list is []:
            return
        for count in count_list:
            item = dict()
            item['title'] = count.xpath('./a/text()').get()
            item['link'] = count.xpath('./a/@href').get()
            item['code'] = re.findall('https://bj.58.com/yewu/pve_5363_244/',item['link'])

            print(item)