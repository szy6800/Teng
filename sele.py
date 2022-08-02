import requests

headers = {
    'authority': 'bj.58.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://bj.58.com/yiyaodaibiao/?key=%E6%8B%9B%E8%81%98&cmcskey=%E6%8B%9B%E8%81%98&final=1&jump=1&specialtype=gls&classpolicy=uuid_cc041b2e40ce4556bbc04ac2e4130ce8,displocalid_1,from_main,to_jump,tradeline_job,classify_D&PGTID=0d30364d-0000-1264-beca-c1556f5c9e06&ClickID=4',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; time_create=1661918604473; userid360_xml=C7977A6730823F910D61E36545E6F68B; id58=CocHKmJrsvwd00/gBFPwAg==; 58tj_uuid=883f06af-ea1f-4366-8018-3e35725400e7; als=0; wmda_uuid=22af24eb753314591c43d6563191d5af; wmda_new_uuid=1; xxzl_deviceid=wb8gy%2FPMsMYQmw%2BwB5TZAOoxa%2B0WEbhPnxMTVNdk5HUwxd%2BheF7itHNXY97solAH; wmda_visited_projects=%3B11187958619315%3B1731916484865%3B2286118353409%3B10104579731767; 58home=bj; f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; commontopbar_ipcity=bj%7C%E5%8C%97%E4%BA%AC%7C0; city=bj; spm=; utm_source=; new_uv=3; init_refer=; wmda_session_id_11187958619315=1659325885286-cdd6b72b-5776-cabf; xxzl_cid=82d0de8097ae4b218bb0cf7518483a55; xzuid=580970d0-7108-4f94-84a5-72a409098990; sessionid=3cda78c2-5f56-4765-a1d9-acb460e821e7; fzq_h=78797577584cb36b3120b130977c468f_1659325897419_9316fa20d68c4432933f14aa927d4e64_2071877498; wmda_session_id_1731916484865=1659325897074-6b52ce6e-ce42-1946; new_session=0; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1659325898; Hm_lvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1659326041; __utma=253535702.71241368.1656061471.1656061471.1659326049.2; __utmc=253535702; __utmz=253535702.1659326049.2.2.utmcsr=qy.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/80531377537556/; __utmt_pageTracker=1; myfeet_tooltip=end; __utmb=253535702.3.10.1659326049; wmda_session_id_2286118353409=1659326139015-ee90f3f7-1334-23e0; fzq_js_infodetailweb=54c6e12bc18018984c0000fe5bd42e7f_1659326163478_9; ppStore_fingerprint=331EA1935B39F35F42D3E8461D1546FBB24A252A5BE5EA8F%EF%BC%BF1659326163533; Hm_lpvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1659326164; JSESSIONID=768042B9B720F708943168AB489AA176; fzq_js_zhaopin_list_pc=fd95e2d1d705031245597ea7d8a3138d_1659326604083_9; Hm_lpvt_5bcc464efd3454091cf2095d3515ea05=1659326604',
}

params = (
    ('key', '\u62DB\u8058'),
    ('cmcskey', '\u62DB\u8058'),
    ('final', '1'),
    ('jump', '1'),
    ('specialtype', 'gls'),
    ('classpolicy', 'uuid_cc041b2e40ce4556bbc04ac2e4130ce8,displocalid_1,from_main,to_jump,tradeline_job,classify_D'),
    ('pid', '452804496442097665'),
    ('PGTID', '0d3029e4-0000-1921-9081-243dc765ea5d'),
    ('ClickID', ''),
)

response = requests.get('https://bj.58.com/yiyaodaibiao/pn7/', headers=headers, params=params)
print(response.text)
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://bj.58.com/yiyaodaibiao/pn2/?key=%E6%8B%9B%E8%81%98&cmcskey=%E6%8B%9B%E8%81%98&final=1&jump=1&specialtype=gls&classpolicy=uuid_cc041b2e40ce4556bbc04ac2e4130ce8,displocalid_1,from_main,to_jump,tradeline_job,classify_D&pid=452804496442097665&PGTID=0d3029e4-0000-1921-9081-243dc765ea5d&ClickID=3', headers=headers)
