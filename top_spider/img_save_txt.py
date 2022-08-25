# coding : utf-8

import requests
import csv
import time




url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin=16750&count=5&fakeid=MjM5NzI3NDg4MA==&type=9&query=&token=1415428887&lang=zh_CN&f=json&ajax=1'

header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3877.400 QQBrowser/10.8.4506.400',
'cookie': 'RK=GrRl30WNQC; ptcz=fd509bf54a54c4c417e353f0035313ed66e2509a7002099a9d14e58731010d7b; pgv_pvi=2382221312; tvfe_boss_uuid=245fd3b0ecc90ae0; ua_id=wra8wh1AdreVykeoAAAAAFKCHwYkPUQGiGpHtz1mvR8=; gr_user_id=1473e4b7-83ef-4a55-b000-f8317900d63b; grwng_uid=7ec4771f-3269-4c3d-a57e-4511c41f5b31; iip=0; mobileUV=1_173b2b7fbd5_50992; pgv_pvid=6285974795; o_cookie=1198558613; wxuin=24518109027797; pac_uid=1_1198558613; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217825c3105a743-0e98dd9807f71f-53e356a-1327104-17825c3105b7c9%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%7D%2C%22%24device_id%22%3A%2217825c3105a743-0e98dd9807f71f-53e356a-1327104-17825c3105b7c9%22%7D; ptui_loginuin=1198558613; sd_userid=30611632635662766; sd_cookie_crttime=1632635662766; AMCV_248F210755B762187F000101%40AdobeOrg=-1712354808%7CMCIDTS%7C18943%7CMCMID%7C31039448042142250641695599293511700131%7CMCAAMLH-1637287116%7C11%7CMCAAMB-1637287116%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1636689516s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.3.0; eas_sid=61x6f3D8c2E4s081z2P552G4i6; pgv_info=ssid=s7325393996; vversion_name=8.2.95; video_omgid=e3ae777b21c3975a; _qpsvr_localtk=0.4719333271591373; uuid=9c5495f333cfc5e0bc7ee94a1aab7481; rand_info=CAESIHPnCa3afChZxodtMBs8B4kB/8+370q8rq+qX+ZiXl0Y; slave_bizuin=3880171456; data_bizuin=3880171456; bizuin=3880171456; data_ticket=8Qhcmpms1CVa+rykPCDhbTG0qva8hD0XiKo8LSiV332jww2HKVgUX/B/XY96uujJ; slave_sid=QUlQYlU5N3huMnIyQ3BoREZzQUZjMmlyR3JLNGM5TUN3QmJjVXJlb3NQWk9yXzVqRmRjdkZJcnRVb21wdEJhT3RGYng3aE5KTXd2dUZsd0ZtOU5uWkQwdjNWTXRDWTdsdnZtYW00SVp0RWVyel9zRlRRa3ZsUldpeW4wbTN1Q3lzSDF0MDdzZW5sR05OZFA2; slave_user=gh_c842d72f86eb; xid=cbd201c5a891942109e4638378052bbc; mm_lang=zh_CN; rewardsn=; wxtokenkey=777'
    }


res = requests.get(url,headers=header)
print(res.text)
