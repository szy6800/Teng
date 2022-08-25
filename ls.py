info = """accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
cache-control: no-cache
cookie: userid360_xml=C7977A6730823F910D61E36545E6F68B; time_create=1663225034203; f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; id58=CocHKmJrsvwd00/gBFPwAg==; 58tj_uuid=883f06af-ea1f-4366-8018-3e35725400e7; als=0; wmda_uuid=22af24eb753314591c43d6563191d5af; wmda_new_uuid=1; xxzl_deviceid=wb8gy%2FPMsMYQmw%2BwB5TZAOoxa%2B0WEbhPnxMTVNdk5HUwxd%2BheF7itHNXY97solAH; 58home=bj; myfeet_tooltip=end; xxzl_smartid=610a42d76847430ba91d9f85189542fc; Hm_lvt_fe7700af2f35759e6256aa5635b9c9ff=1659340591; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1659340632; final_history=47907462014755; city=bj; wmda_visited_projects=%3B11187958619315%3B1731916484865%3B2286118353409%3B10104579731767%3B1409632296065%3B2385390625025; __utma=253535702.71241368.1656061471.1661323387.1661326720.7; __utmz=253535702.1661326720.7.7.utmcsr=qy.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/bj_245/; myLat=""; myLon=""; mcity=bj; f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; commontopbar_ipcity=bj%7C%E5%8C%97%E4%BA%AC%7C0; xxzl_cid=82d0de8097ae4b218bb0cf7518483a55; xzuid=580970d0-7108-4f94-84a5-72a409098990; sessionid=072516b5-c9cd-42ef-b87f-c9c389c9e139; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1660644768,1660704526,1661311396,1661393627; Hm_lvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1660289005,1660543846,1661308181,1661393630; fzq_h=5ac02eaef2c163186680c4c5dd8763d0_1661396099938_5a077ec166bc482da1a0f2dc495cd2be_2071877498; www58com="UserID=71458147739661&UserName=0fxbux8ev"; 58cooper="userid=71458147739661&username=0fxbux8ev"; 58uname=0fxbux8ev; passportAccount="atype=0&bstate=0"; wmda_session_id_1731916484865=1661417318377-0eeb0a3f-e9f5-c273; new_uv=26; utm_source=; spm=; init_refer=https%253A%252F%252Fcallback.58.com%252F; wmda_session_id_11187958619315=1661417319688-bd9d9811-348d-954b; new_session=0; PPU.sig=xt9Aw3HVC5_443PHBDthgFaQ_ko; Hm_lpvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1661417373; fzq_js_infodetailweb=6bc776e1d1b833d07dbfa5769f3415b0_1661417373037_9; ppStore_fingerprint=331EA1935B39F35F42D3E8461D1546FBB24A252A5BE5EA8F%EF%BC%BF1661417373082; JSESSIONID=5FCCBFD585F0A57D9067CDC756B24535; fzq_js_zhaopin_list_pc=abcb276604941a2efc71b7964268a57d_1661417413025_7; Hm_lpvt_5bcc464efd3454091cf2095d3515ea05=1661417413; PPU=UID=71458147739661&UN=0fxbux8ev&TT=ed2c17ffbc45e3b974e47ddab003c26e&PBODY=WKWT2YYepn6vxy1zUpDPYVX3oh_8iY_NbNrKhJk11Ow-oJWNTJIUo76RRNp8bSNTvh8-cMIob9a03Dib6oC8jMguhqW9pHrigWIfEVFfbuTGwqmMp-_QoyD2oL1sAHqhRJMufkPofR3Hu-TuG1R6hhJziTvnOFd-lLf5NUTTerQ&VER=1&CUID=Ia5GM2c1i47263wLL87x3w
pragma: no-cache
referer: https://callback.58.com/
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: same-site
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"""
headers = {}
for i in info.split('\n'):
    a = i.split(': ',1)
    headers[a[0]]=a[1]

print(headers)
