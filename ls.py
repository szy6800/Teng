info = """accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
cache-control: no-cache
cookie: time_create=1661924477382; userid360_xml=C7977A6730823F910D61E36545E6F68B; f=n; commontopbar_new_city_info=1%7C%E5%8C%97%E4%BA%AC%7Cbj; commontopbar_ipcity=bj%7C%E5%8C%97%E4%BA%AC%7C0; SECKEY_ABVK=DUgxuaSXTX2L4Xn0jnvs885jlTRHHjYLG8OPjAyPBpw%3D; BMAP_SECKEY=wkT-bogpsnQn7FNJ1tIvLXARE0gSftEFwMlMPmbaoL6hUnOldEn5EJZo9himc3M2l190pvZm0jsP1GsWDeWYQHSTSq7MikfnqzB7X8PjKf_9Fp33kFu0yvjDWNTXWJRgEnev1RHqcDLOp2q8Q_awd4EvBqoAs7dW1wMe57l58ZNfXkUqQryr7lWZshAQklza; id58=CocHKmJrsvwd00/gBFPwAg==; 58tj_uuid=883f06af-ea1f-4366-8018-3e35725400e7; als=0; wmda_uuid=22af24eb753314591c43d6563191d5af; wmda_new_uuid=1; xxzl_deviceid=wb8gy%2FPMsMYQmw%2BwB5TZAOoxa%2B0WEbhPnxMTVNdk5HUwxd%2BheF7itHNXY97solAH; 58home=bj; myfeet_tooltip=end; xxzl_smartid=610a42d76847430ba91d9f85189542fc; Hm_lvt_fe7700af2f35759e6256aa5635b9c9ff=1659340591; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1659340632; final_history=47907462014755; city=bj; wmda_visited_projects=%3B11187958619315%3B1731916484865%3B2286118353409%3B10104579731767%3B1409632296065%3B2385390625025; xxzl_cid=82d0de8097ae4b218bb0cf7518483a55; xzuid=580970d0-7108-4f94-84a5-72a409098990; Hm_lvt_5bcc464efd3454091cf2095d3515ea05=1660283975,1660632208,1660644768,1660704526; __utma=253535702.71241368.1656061471.1660637082.1660704556.5; __utmz=253535702.1660704556.5.5.utmcsr=qy.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/79246787742762/; fzq_h=e66f5b52cdbd874ec3e90094c9b88a5c_1661307809766_33929f8926fa43ec9b6093984ceb9c1f_2071877498; www58com="UserID=71458147739661&UserName=0fxbux8ev"; 58cooper="userid=71458147739661&username=0fxbux8ev"; 58uname=0fxbux8ev; passportAccount="atype=0&bstate=0"; PPU=UID=71458147739661&UN=0fxbux8ev&TT=1a45585d05736b4306d8c9cbe2596de7&PBODY=KouRcYz5jC9KzwExVjtIVBbLRwVLZ9hMPwbg2nL8ldvagm8NBEXADwLH3OWOP0JQvK1WveR_18Ux2aDk1ME9vXS259rbXvp0evKSUa0P4fwsy2_Ii6Nrk1Bn9J2wOLHtcjDmXKnqXHcBunhn4zxSbRWlnPm7jlUVzBPpOW8Lpbg&VER=1&CUID=Ia5GM2c1i47263wLL87x3w; sessionid=7b8674fc-7456-41d0-b08b-74db14aa8f99; wmda_session_id_1731916484865=1661308180401-98ca11d1-3c4a-472e; Hm_lpvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1661308181; Hm_lvt_b2c7b5733f1b8ddcfc238f97b417f4dd=1660204241,1660289005,1660543846,1661308181; new_session=1; new_uv=21; utm_source=; spm=; init_refer=https%253A%252F%252Fcallback.58.com%252F; fzq_js_infodetailweb=381c6f19d262c997b829d9bb0441b2ce_1661308180651_6; f=n; PPU.sig=yOHcHR20HdsI0h-kICyfzZ_yCjA; wmda_session_id_11187958619315=1661308181277-91d4e3a0-8daa-88db; ppStore_fingerprint=331EA1935B39F35F42D3E8461D1546FBB24A252A5BE5EA8F%EF%BC%BF1661308181651
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
