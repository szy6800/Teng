# -*- coding: utf-8 -*-

# @Time : 2022/3/17 9:57
# @Author : 石张毅
# @Site : 
# @File : sele.py
# @Software: PyCharm 
from fake_useragent import UserAgent
# from selenium.webdriver.common.by import By
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# chrome_options = Options()
# chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
# # chrome_options.add_argument("--headless")
# chrome_options.headless = True
# chrome_options.add_argument('window-size=1400x1015')  # 指定浏览器分辨率
# chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
# chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
# chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
# chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
# chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
# chrome_options.add_argument('--start-maximized')  # 浏览器最大化
# chrome_options.add_argument('--window-size=1280x1024')  # 设置浏览器分辨率（窗口大小）
# chrome_options.add_argument('log-level=3')
# chrome_options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
# chrome_options.add_argument('--incognito')  # 隐身模式（无痕模式）
# chrome_options.add_argument('--disable-javascript')  # 禁用javascript
# chrome_options.add_argument('--ignore-certificate-errors')  # 禁用扩展插件并实现窗口最大化
# chrome_options.add_argument('–disable-software-rasterizer')
# chrome_options.add_argument('--disable-extensions')
# chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit'
#                             f'/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36')
# chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
# chrome_options.add_experimental_option('useAutomationExtension', False)
# browser = webdriver.Chrome(options=chrome_options)
# browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#     "source": """
#     Object.defineProperty(navigator, 'webdriver', {
#       get: () => undefined
#     })
#   """
# })
# import time
# browser.get('https://cg.95306.cn/')
# for page in range(1,5):
#     time.sleep(2)
#     nwepage = browser.find_element(by=By.PARTIAL_LINK_TEXT, value='下一页')
#     nwepage.click()
#     time.sleep(2)

import requests
from lxml import etree
import re


def get_city():
    url = 'http://www.iecity.com/CityList/map/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    res.encoding = res.apparent_encoding
    html = etree.HTML(res.text)
    provice = html.xpath('//*[@class="CityList"]//*[@class="Province"]/text()')

    city = html.xpath('//*[@class="CityList"]//a/text()')
    # print(city)

    city_href = html.xpath('//*[@class="CityList"]//a/@href')
    count = 0
    city_list = []
    for city,city_href, in zip(city,city_href):
        item = {}
        city_hrefs = re.findall(r'http://www.iecity.com/(.*?)/map/', city_href)[0]
        city_href = 'http://www.iecity.com/'+city_hrefs+'/map/Road---b4e5d7af--1.html'
        # print(city_href)
        res = requests.get(city_href, headers=headers)
        res.encoding = res.apparent_encoding
        res = res.text
        # print(res)
        try:
            pages = re.findall(r'当前在第 .* 页 共计 (.*?) 个页面 共有 .* 条记录', res)[0]
        except:
            item['page'] = '0'
        else:
            item['provincial_capital'] = city
            item['url'] = city_hrefs
            item['page'] = int(pages)+1
            count += 1
            city_list.append(item)
            print(count,item)
    print(city_list)


get_city()

# [{'provincial_capital': '澳门', 'url': 'http://www.iecity.com/aomen/map/Road---b4e5d7af--1.html', 'page': '1'},
#  {'provincial_capital': '合肥', 'url': 'http://www.iecity.com/hefei/map/Road---b4e5d7af--1.html', 'page': '73'},
#  {'provincial_capital': '蚌埠', 'url': 'http://www.iecity.com/bangbu/map/Road---b4e5d7af--1.html', 'page': '24'},
#  {'provincial_capital': '芜湖', 'url': 'http://www.iecity.com/wuhu/map/Road---b4e5d7af--1.html', 'page': '37'},
#  {'provincial_capital': '马鞍山', 'url': 'http://www.iecity.com/maanshan/map/Road---b4e5d7af--1.html', 'page': '23'},
#  {'provincial_capital': '安庆', 'url': 'http://www.iecity.com/anqing/map/Road---b4e5d7af--1.html', 'page': '50'},
#  {'provincial_capital': '黄山', 'url': 'http://www.iecity.com/huangshan/map/Road---b4e5d7af--1.html', 'page': '37'},
#  {'provincial_capital': '巢湖', 'url': 'http://www.iecity.com/chaohu/map/Road---b4e5d7af--1.html', 'page': '0'},
#  {'provincial_capital': '亳州', 'url': 'http://www.iecity.com/haozhou/map/Road---b4e5d7af--1.html', 'page': '39'},
#  {'provincial_capital': '六安', 'url': 'http://www.iecity.com/liuan/map/Road---b4e5d7af--1.html', 'page': '47'},
#  {'provincial_capital': '宣城', 'url': 'http://www.iecity.com/xuancheng/map/Road---b4e5d7af--1.html', 'page': '29'},
#  {'provincial_capital': '宿州', 'url': 'http://www.iecity.com/suuzhou/map/Road---b4e5d7af--1.html', 'page': '40'},
#  {'provincial_capital': '池州', 'url': 'http://www.iecity.com/chizhou/map/Road---b4e5d7af--1.html', 'page': '28'},
#  {'provincial_capital': '淮北', 'url': 'http://www.iecity.com/huaibei/map/Road---b4e5d7af--1.html', 'page': '16'},
#  {'provincial_capital': '淮南', 'url': 'http://www.iecity.com/huainan/map/Road---b4e5d7af--1.html', 'page': '19'},
#  {'provincial_capital': '滁州', 'url': 'http://www.iecity.com/chuzhou/map/Road---b4e5d7af--1.html', 'page': '41'},
#  {'provincial_capital': '铜陵', 'url': 'http://www.iecity.com/tongling/map/Road---b4e5d7af--1.html', 'page': '13'},
#  {'provincial_capital': '阜阳', 'url': 'http://www.iecity.com/fuyang/map/Road---b4e5d7af--1.html', 'page': '39'},
#  {'provincial_capital': '福州', 'url': 'http://www.iecity.com/fuzhou/map/Road---b4e5d7af--1.html', 'page': '46'},
#  {'provincial_capital': '厦门', 'url': 'http://www.iecity.com/xiamen/map/Road---b4e5d7af--1.html', 'page': '23'},
#  {'provincial_capital': '宁德', 'url': 'http://www.iecity.com/ningde/map/Road---b4e5d7af--1.html', 'page': '29'},
#  {'provincial_capital': '莆田', 'url': 'http://www.iecity.com/putian/map/Road---b4e5d7af--1.html', 'page': '19'},
#  {'provincial_capital': '泉州', 'url': 'http://www.iecity.com/quanzhou/map/Road---b4e5d7af--1.html', 'page': '38'},
#  {'provincial_capital': '漳州', 'url': 'http://www.iecity.com/zhangzhou/map/Road---b4e5d7af--1.html', 'page': '26'},
#  {'provincial_capital': '三明', 'url': 'http://www.iecity.com/sanming/map/Road---b4e5d7af--1.html', 'page': '28'},
#  {'provincial_capital': '南平', 'url': 'http://www.iecity.com/nanping/map/Road---b4e5d7af--1.html', 'page': '26'},
#  {'provincial_capital': '龙岩', 'url': 'http://www.iecity.com/longyan/map/Road---b4e5d7af--1.html', 'page': '23'},
#  {'provincial_capital': '深圳', 'url': 'http://www.iecity.com/shenzhen/map/Road---b4e5d7af--1.html', 'page': '25'},
#  {'provincial_capital': '珠海', 'url': 'http://www.iecity.com/zhuhai/map/Road---b4e5d7af--1.html', 'page': '14'},
#  {'provincial_capital': '佛山', 'url': 'http://www.iecity.com/foshan/map/Road---b4e5d7af--1.html', 'page': '36'},
#  {'provincial_capital': '肇庆', 'url': 'http://www.iecity.com/zhaoqing/map/Road---b4e5d7af--1.html', 'page': '38'},
#  {'provincial_capital': '汕头', 'url': 'http://www.iecity.com/shantou/map/Road---b4e5d7af--1.html', 'page': '18'},
#  {'provincial_capital': '湛江', 'url': 'http://www.iecity.com/zhanjiang/map/Road---b4e5d7af--1.html', 'page': '25'},
#  {'provincial_capital': '中山', 'url': 'http://www.iecity.com/zhongshan/map/Road---b4e5d7af--1.html', 'page': '18'},
#  {'provincial_capital': '潮州', 'url': 'http://www.iecity.com/chaozhou/map/Road---b4e5d7af--1.html', 'page': '19'},
#  {'provincial_capital': '东莞', 'url': 'http://www.iecity.com/dongguan/map/Road---b4e5d7af--1.html', 'page': '22'},
#  {'provincial_capital': '阳江', 'url': 'http://www.iecity.com/yangjiang/map/Road---b4e5d7af--1.html', 'page': '24'},
#  {'provincial_capital': '揭阳', 'url': 'http://www.iecity.com/jieyang/map/Road---b4e5d7af--1.html', 'page': '18'},
#  {'provincial_capital': '茂名', 'url': 'http://www.iecity.com/maoming/map/Road---b4e5d7af--1.html', 'page': '38'},
#  {'provincial_capital': '江门', 'url': 'http://www.iecity.com/jiangmen/map/Road---b4e5d7af--1.html', 'page': '38'},
#  {'provincial_capital': '韶关', 'url': 'http://www.iecity.com/shaoguan/map/Road---b4e5d7af--1.html', 'page': '37'},
#  {'provincial_capital': '惠州', 'url': 'http://www.iecity.com/huizhou/map/Road---b4e5d7af--1.html', 'page': '45'},
#  {'provincial_capital': '梅州', 'url': 'http://www.iecity.com/meizhou/map/Road---b4e5d7af--1.html', 'page': '56'},
#  {'provincial_capital': '云浮', 'url': 'http://www.iecity.com/yunfu/map/Road---b4e5d7af--1.html', 'page': '32'},
#  {'provincial_capital': '河源', 'url': 'http://www.iecity.com/heyuan/map/Road---b4e5d7af--1.html', 'page': '39'},
#  {'provincial_capital': '清远', 'url': 'http://www.iecity.com/qingyuan/map/Road---b4e5d7af--1.html', 'page': '66'},
#  {'provincial_capital': '南宁', 'url': 'http://www.iecity.com/nanning/map/Road---b4e5d7af--1.html', 'page': '39'},
#  {'provincial_capital': '柳州', 'url': 'http://www.iecity.com/liuzhou/map/Road---b4e5d7af--1.html', 'page': '31'},
#  {'provincial_capital': '桂林', 'url': 'http://www.iecity.com/guilin/map/Road---b4e5d7af--1.html', 'page': '60'},
#  {'provincial_capital': '北海', 'url': 'http://www.iecity.com/beihai/map/Road---b4e5d7af--1.html', 'page': '13'},
#  {'provincial_capital': '防城港', 'url': 'http://www.iecity.com/fangchenggang/map/Road---b4e5d7af--1.html',
#   'page': '17'},
#  {'provincial_capital': '崇左', 'url': 'http://www.iecity.com/chongzuo/map/Road---b4e5d7af--1.html', 'page': '21'},
#  {'provincial_capital': '来宾', 'url': 'http://www.iecity.com/laibin/map/Road---b4e5d7af--1.html', 'page': '17'},
#  {'provincial_capital': '梧州', 'url': 'http://www.iecity.com/wuzhou/map/Road---b4e5d7af--1.html', 'page': '23'},
#  {'provincial_capital': '河池', 'url': 'http://www.iecity.com/hechi/map/Road---b4e5d7af--1.html', 'page': '57'},
#  {'provincial_capital': '玉林', 'url': 'http://www.iecity.com/yulin/map/Road---b4e5d7af--1.html', 'page': '34'},
#  {'provincial_capital': '贵港', 'url': 'http://www.iecity.com/guigang/map/Road---b4e5d7af--1.html', 'page': '35'},
#  {'provincial_capital': '贺州', 'url': 'http://www.iecity.com/hezhou/map/Road---b4e5d7af--1.html', 'page': '32'},
#  {'provincial_capital': '钦州', 'url': 'http://www.iecity.com/qinzhou/map/Road---b4e5d7af--1.html', 'page': '31'},
#  {'provincial_capital': '百色', 'url': 'http://www.iecity.com/baise/map/Road---b4e5d7af--1.html', 'page': '26'},
#  {'provincial_capital': '贵阳', 'url': 'http://www.iecity.com/guiyang/map/Road---b4e5d7af--1.html', 'page': '38'},
#  {'provincial_capital': '安顺', 'url': 'http://www.iecity.com/anshun/map/Road---b4e5d7af--1.html', 'page': '33'},
#  {'provincial_capital': '毕节地区', 'url': 'http://www.iecity.com/bijie/map/Road---b4e5d7af--1.html', 'page': '28'},
#  {'provincial_capital': '遵义', 'url': 'http://www.iecity.com/zunyi/map/Road---b4e5d7af--1.html', 'page': '88'},
#  {'provincial_capital': '铜仁地区', 'url': 'http://www.iecity.com/tongren/map/Road---b4e5d7af--1.html', 'page': '22'},
#  {'provincial_capital': '黔东南', 'url': 'http://www.iecity.com/qiandongnan/map/Road---b4e5d7af--1.html',
#   'page': '39'},
#  {'provincial_capital': '黔南', 'url': 'http://www.iecity.com/qiannan/map/Road---b4e5d7af--1.html', 'page': '35'},
#  {'provincial_capital': '六盘水', 'url': 'http://www.iecity.com/liupanshui/map/Road---b4e5d7af--1.html',
#   'page': '25'},
#  {'provincial_capital': '黔西南州', 'url': 'http://www.iecity.com/qianxinanzhou/map/Road---b4e5d7af--1.html',
#   'page': '28'},
#  {'provincial_capital': '兰州', 'url': 'http://www.iecity.com/lanzhou/map/Road---b4e5d7af--1.html', 'page': '46'},
#  {'provincial_capital': '定西', 'url': 'http://www.iecity.com/dingxi/map/Road---b4e5d7af--1.html', 'page': '44'},
#  {'provincial_capital': '平凉', 'url': 'http://www.iecity.com/pingliang/map/Road---b4e5d7af--1.html', 'page': '26'},
#  {'provincial_capital': '庆阳', 'url': 'http://www.iecity.com/qingyang/map/Road---b4e5d7af--1.html', 'page': '47'},
#  {'provincial_capital': '张掖', 'url': 'http://www.iecity.com/zhangye/map/Road---b4e5d7af--1.html', 'page': '26'},
#  {'provincial_capital': '武威', 'url': 'http://www.iecity.com/wuwei/map/Road---b4e5d7af--1.html', 'page': '29'},
#  {'provincial_capital': '白银', 'url': 'http://www.iecity.com/baiyin/map/Road---b4e5d7af--1.html', 'page': '26'},
#  {'provincial_capital': '酒泉', 'url': 'http://www.iecity.com/jiuquan/map/Road---b4e5d7af--1.html', 'page': '15'},
#  {'provincial_capital': '金昌', 'url': 'http://www.iecity.com/jinchang/map/Road---b4e5d7af--1.html', 'page': '10'},
#  {'provincial_capital': '陇南', 'url': 'http://www.iecity.com/longnan/map/Road---b4e5d7af--1.html', 'page': '37'},
#  {'provincial_capital': '临夏', 'url': 'http://www.iecity.com/linxia/map/Road---b4e5d7af--1.html', 'page': '25'},
#  {'provincial_capital': '甘南州', 'url': 'http://www.iecity.com/gannanzhou/map/Road---b4e5d7af--1.html',
#   'page': '18'},
#  {'provincial_capital': '嘉峪关', 'url': 'http://www.iecity.com/jiayuguan/map/Road---b4e5d7af--1.html', 'page': '3'},
#  {'provincial_capital': '邯郸', 'url': 'http://www.iecity.com/handan/map/Road---b4e5d7af--1.html', 'page': '42'},
#  {'provincial_capital': '石家庄', 'url': 'http://www.iecity.com/shijiazhuang/map/Road---b4e5d7af--1.html',
#   'page': '38'},
#  {'provincial_capital': '保定', 'url': 'http://www.iecity.com/baoding/map/Road---b4e5d7af--1.html', 'page': '58'},
#  {'provincial_capital': '张家口', 'url': 'http://www.iecity.com/zhangjiakou/map/Road---b4e5d7af--1.html',
#   'page': '30'},
#  {'provincial_capital': '承德', 'url': 'http://www.iecity.com/chengde/map/Road---b4e5d7af--1.html', 'page': '58'},
#  {'provincial_capital': '唐山', 'url': 'http://www.iecity.com/tangshan/map/Road---b4e5d7af--1.html', 'page': '33'},
#  {'provincial_capital': '廊坊', 'url': 'http://www.iecity.com/langfang/map/Road---b4e5d7af--1.html', 'page': '19'},
#  {'provincial_capital': '秦皇岛', 'url': 'http://www.iecity.com/qinhuangdao/map/Road---b4e5d7af--1.html',
#   'page': '20'},
#  {'provincial_capital': '沧州', 'url': 'http://www.iecity.com/cangzhou/map/Road---b4e5d7af--1.html', 'page': '29'},
#  {'provincial_capital': '衡水', 'url': 'http://www.iecity.com/hengshui/map/Road---b4e5d7af--1.html', 'page': '39'},
#  {'provincial_capital': '邢台', 'url': 'http://www.iecity.com/xingtai/map/Road---b4e5d7af--1.html', 'page': '34'},
#  {'provincial_capital': '郑州', 'url': 'http://www.iecity.com/zhengzhou/map/Road---b4e5d7af--1.html', 'page': '36'},
#  {'provincial_capital': '安阳', 'url': 'http://www.iecity.com/anyang/map/Road---b4e5d7af--1.html', 'page': '25'},
#  {'provincial_capital': '新乡', 'url': 'http://www.iecity.com/xinxiang/map/Road---b4e5d7af--1.html', 'page': '24'},
#  {'provincial_capital': '许昌', 'url': 'http://www.iecity.com/xuchang/map/Road---b4e5d7af--1.html', 'page': '22'},
#  {'provincial_capital': '平顶山', 'url': 'http://www.iecity.com/pingdingshan/map/Road---b4e5d7af--1.html',
#   'page': '25'},
#  {'provincial_capital': '开封', 'url': 'http://www.iecity.com/kaifeng/map/Road---b4e5d7af--1.html', 'page': '35'},
#  {'provincial_capital': '洛阳', 'url': 'http://www.iecity.com/luoyang/map/Road---b4e5d7af--1.html', 'page': '50'},
#  {'provincial_capital': '焦作', 'url': 'http://www.iecity.com/jiaozuo/map/Road---b4e5d7af--1.html', 'page': '20'},
#  {'provincial_capital': '三门峡', 'url': 'http://www.iecity.com/sanmenxia/map/Road---b4e5d7af--1.html', 'page': '28'},
#  {'provincial_capital': '信阳', 'url': 'http://www.iecity.com/xinyang/map/Road---b4e5d7af--1.html', 'page': '44'},
#  {'provincial_capital': '南阳', 'url': 'http://www.iecity.com/nanyang/map/Road---b4e5d7af--1.html', 'page': '50'},
#  {'provincial_capital': '周口', 'url': 'http://www.iecity.com/zhoukou/map/Road---b4e5d7af--1.html', 'page': '29'},
#  {'provincial_capital': '商丘', 'url': 'http://www.iecity.com/shangqiu/map/Road---b4e5d7af--1.html', 'page': '38'},
#  {'provincial_capital': '济源', 'url': 'http://www.iecity.com/jiyuan/map/Road---b4e5d7af--1.html', 'page': '21'},
#  {'provincial_capital': '漯河', 'url': 'http://www.iecity.com/luohe/map/Road---b4e5d7af--1.html', 'page': '18'},
#  {'provincial_capital': '濮阳', 'url': 'http://www.iecity.com/puyang/map/Road---b4e5d7af--1.html', 'page': '26'},
#  {'provincial_capital': '驻马店', 'url': 'http://www.iecity.com/zhumadian/map/Road---b4e5d7af--1.html', 'page': '39'},
#  {'provincial_capital': '鹤壁', 'url': 'http://www.iecity.com/hebi/map/Road---b4e5d7af--1.html', 'page': '12'},
#  {'provincial_capital': '武汉', 'url': 'http://www.iecity.com/wuhan/map/Road---b4e5d7af--1.html', 'page': '47'},
#  {'provincial_capital': '襄樊', 'url': 'http://www.iecity.com/xiangfan/map/Road---b4e5d7af--1.html', 'page': '27'},
#  {'provincial_capital': '鄂州', 'url': 'http://www.iecity.com/ezhou/map/Road---b4e5d7af--1.html', 'page': '18'},
#  {'provincial_capital': '荆州', 'url': 'http://www.iecity.com/jingzhou/map/Road---b4e5d7af--1.html', 'page': '35'},
#  {'provincial_capital': '宜昌', 'url': 'http://www.iecity.com/yichang/map/Road---b4e5d7af--1.html', 'page': '70'},
#  {'provincial_capital': '十堰', 'url': 'http://www.iecity.com/shiyan/map/Road---b4e5d7af--1.html', 'page': '70'},
#  {'provincial_capital': '荆门', 'url': 'http://www.iecity.com/jingmen/map/Road---b4e5d7af--1.html', 'page': '32'},
#  {'provincial_capital': '仙桃', 'url': 'http://www.iecity.com/xiantao/map/Road---b4e5d7af--1.html', 'page': '14'},
#  {'provincial_capital': '咸宁', 'url': 'http://www.iecity.com/xianning/map/Road---b4e5d7af--1.html', 'page': '25'},
#  {'provincial_capital': '天门', 'url': 'http://www.iecity.com/tianmen/map/Road---b4e5d7af--1.html', 'page': '18'},
#  {'provincial_capital': '孝感', 'url': 'http://www.iecity.com/xiaogan/map/Road---b4e5d7af--1.html', 'page': '32'},
#  {'provincial_capital': '潜江', 'url': 'http://www.iecity.com/qianjiang/map/Road---b4e5d7af--1.html', 'page': '12'},
#  {'provincial_capital': '随州', 'url': 'http://www.iecity.com/suizhou/map/Road---b4e5d7af--1.html', 'page': '39'},
#  {'provincial_capital': '黄冈', 'url': 'http://www.iecity.com/huanggang/map/Road---b4e5d7af--1.html', 'page': '57'},
#  {'provincial_capital': '神农架', 'url': 'http://www.iecity.com/shennongjia/map/Road---b4e5d7af--1.html',
#   'page': '9'},
#  {'provincial_capital': '恩施', 'url': 'http://www.iecity.com/enshi/map/Road---b4e5d7af--1.html', 'page': '48'},
#  {'provincial_capital': '岳阳', 'url': 'http://www.iecity.com/yueyang/map/Road---b4e5d7af--1.html', 'page': '48'},
#  {'provincial_capital': '长沙', 'url': 'http://www.iecity.com/changsha/map/Road---b4e5d7af--1.html', 'page': '65'},
#  {'provincial_capital': '湘潭', 'url': 'http://www.iecity.com/xiangtan/map/Road---b4e5d7af--1.html', 'page': '33'},
#  {'provincial_capital': '株洲', 'url': 'http://www.iecity.com/zhuzhou/map/Road---b4e5d7af--1.html', 'page': '71'},
#  {'provincial_capital': '衡阳', 'url': 'http://www.iecity.com/hengyang/map/Road---b4e5d7af--1.html', 'page': '47'},
#  {'provincial_capital': '常德', 'url': 'http://www.iecity.com/changde/map/Road---b4e5d7af--1.html', 'page': '47'},
#  {'provincial_capital': '张家界', 'url': 'http://www.iecity.com/zhangjiajie/map/Road---b4e5d7af--1.html',
#   'page': '21'},
#  {'provincial_capital': '娄底', 'url': 'http://www.iecity.com/loudi/map/Road---b4e5d7af--1.html', 'page': '34'},
#  {'provincial_capital': '怀化', 'url': 'http://www.iecity.com/huaihua/map/Road---b4e5d7af--1.html', 'page': '74'},
#  {'provincial_capital': '永州', 'url': 'http://www.iecity.com/yongzhou/map/Road---b4e5d7af--1.html', 'page': '73'},
#  {'provincial_capital': '益阳', 'url': 'http://www.iecity.com/yiyang/map/Road---b4e5d7af--1.html', 'page': '32'},
#  {'provincial_capital': '邵阳', 'url': 'http://www.iecity.com/shaoyang/map/Road---b4e5d7af--1.html', 'page': '36'},
#  {'provincial_capital': '郴州', 'url': 'http://www.iecity.com/chenzhou/map/Road---b4e5d7af--1.html', 'page': '42'},
#  {'provincial_capital': '湘西', 'url': 'http://www.iecity.com/xiangxi/map/Road---b4e5d7af--1.html', 'page': '15'},
#  {'provincial_capital': '哈尔滨', 'url': 'http://www.iecity.com/haerbin/map/Road---b4e5d7af--1.html', 'page': '40'},
#  {'provincial_capital': '齐齐哈尔', 'url': 'http://www.iecity.com/qiqihaer/map/Road---b4e5d7af--1.html', 'page': '27'},
#  {'provincial_capital': '牡丹江', 'url': 'http://www.iecity.com/mudanjiang/map/Road---b4e5d7af--1.html',
#   'page': '17'},
#  {'provincial_capital': '大庆', 'url': 'http://www.iecity.com/daqing/map/Road---b4e5d7af--1.html', 'page': '14'},
#  {'provincial_capital': '佳木斯', 'url': 'http://www.iecity.com/jiamusi/map/Road---b4e5d7af--1.html', 'page': '18'},
#  {'provincial_capital': '七台河', 'url': 'http://www.iecity.com/qitaihe/map/Road---b4e5d7af--1.html', 'page': '4'},
#  {'provincial_capital': '伊春', 'url': 'http://www.iecity.com/yichun/map/Road---b4e5d7af--1.html', 'page': '7'},
#  {'provincial_capital': '双鸭山', 'url': 'http://www.iecity.com/shuangyashan/map/Road---b4e5d7af--1.html',
#   'page': '9'},
#  {'provincial_capital': '大兴安岭', 'url': 'http://www.iecity.com/daxinganling/map/Road---b4e5d7af--1.html',
#   'page': '3'},
#  {'provincial_capital': '绥化', 'url': 'http://www.iecity.com/suihua/map/Road---b4e5d7af--1.html', 'page': '31'},
#  {'provincial_capital': '鸡西', 'url': 'http://www.iecity.com/jixi/map/Road---b4e5d7af--1.html', 'page': '12'},
#  {'provincial_capital': '鹤岗', 'url': 'http://www.iecity.com/hegang/map/Road---b4e5d7af--1.html', 'page': '9'},
#  {'provincial_capital': '黑河', 'url': 'http://www.iecity.com/heihe/map/Road---b4e5d7af--1.html', 'page': '14'},
#  {'provincial_capital': '海口', 'url': 'http://www.iecity.com/haikou/map/Road---b4e5d7af--1.html', 'page': '15'},
#  {'provincial_capital': '三亚', 'url': 'http://www.iecity.com/sanya/map/Road---b4e5d7af--1.html', 'page': '11'},
#  {'provincial_capital': '白沙', 'url': 'http://www.iecity.com/baishaxian/map/Road---b4e5d7af--1.html', 'page': '7'},
#  {'provincial_capital': '保亭', 'url': 'http://www.iecity.com/baotingxian/map/Road---b4e5d7af--1.html', 'page': '8'},
#  {'provincial_capital': '昌江', 'url': 'http://www.iecity.com/changjiangxian/map/Road---b4e5d7af--1.html',
#   'page': '4'},
#  {'provincial_capital': '澄迈', 'url': 'http://www.iecity.com/chengmaixian/map/Road---b4e5d7af--1.html',
#   'page': '9'},
#  {'provincial_capital': '定安', 'url': 'http://www.iecity.com/dinganxian/map/Road---b4e5d7af--1.html', 'page': '9'},
#  {'provincial_capital': '东方', 'url': 'http://www.iecity.com/dongfang/map/Road---b4e5d7af--1.html', 'page': '5'},
#  {'provincial_capital': '乐东', 'url': 'http://www.iecity.com/ledong/map/Road---b4e5d7af--1.html', 'page': '11'},
#  {'provincial_capital': '临高县', 'url': 'http://www.iecity.com/lingaoxian/map/Road---b4e5d7af--1.html',
#   'page': '14'},
#  {'provincial_capital': '陵水', 'url': 'http://www.iecity.com/lingshui/map/Road---b4e5d7af--1.html', 'page': '8'},
#  {'provincial_capital': '琼海', 'url': 'http://www.iecity.com/qionghai/map/Road---b4e5d7af--1.html', 'page': '14'},
#  {'provincial_capital': '琼中', 'url': 'http://www.iecity.com/qiongzhong/map/Road---b4e5d7af--1.html', 'page': '11'},
#  {'provincial_capital': '屯昌县', 'url': 'http://www.iecity.com/tunchangxian/map/Road---b4e5d7af--1.html',
#   'page': '8'},
#  {'provincial_capital': '万宁', 'url': 'http://www.iecity.com/wanning/map/Road---b4e5d7af--1.html', 'page': '9'},
#  {'provincial_capital': '文昌', 'url': 'http://www.iecity.com/wenchang/map/Road---b4e5d7af--1.html', 'page': '14'},
#  {'provincial_capital': '五指山', 'url': 'http://www.iecity.com/wuzhishan/map/Road---b4e5d7af--1.html', 'page': '5'},
#  {'provincial_capital': '儋州', 'url': 'http://www.iecity.com/danzhou/map/Road---b4e5d7af--1.html', 'page': '16'},
#  {'provincial_capital': '三沙', 'url': 'http://www.iecity.com/sansha/map/Road---b4e5d7af--1.html', 'page': '0'},
#  {'provincial_capital': '长春', 'url': 'http://www.iecity.com/changchun/map/Road---b4e5d7af--1.html', 'page': '36'},
#  {'provincial_capital': '吉林', 'url': 'http://www.iecity.com/jilin/map/Road---b4e5d7af--1.html', 'page': '23'},
#  {'provincial_capital': '四平', 'url': 'http://www.iecity.com/siping/map/Road---b4e5d7af--1.html', 'page': '21'},
#  {'provincial_capital': '延边', 'url': 'http://www.iecity.com/yanbian/map/Road---b4e5d7af--1.html', 'page': '8'},
#  {'provincial_capital': '松原', 'url': 'http://www.iecity.com/songyuan/map/Road---b4e5d7af--1.html', 'page': '11'},
#  {'provincial_capital': '白城', 'url': 'http://www.iecity.com/baicheng/map/Road---b4e5d7af--1.html', 'page': '17'},
#  {'provincial_capital': '白山', 'url': 'http://www.iecity.com/baishan/map/Road---b4e5d7af--1.html', 'page': '11'},
#  {'provincial_capital': '辽源', 'url': 'http://www.iecity.com/liaoyuan/map/Road---b4e5d7af--1.html', 'page': '17'},
#  {'provincial_capital': '通化', 'url': 'http://www.iecity.com/tonghua/map/Road---b4e5d7af--1.html', 'page': '14'},
#  {'provincial_capital': '南京', 'url': 'http://www.iecity.com/nanjing/map/Road---b4e5d7af--1.html', 'page': '60'},
#  {'provincial_capital': '无锡', 'url': 'http://www.iecity.com/wuxi/map/Road---b4e5d7af--1.html', 'page': '42'},
#  {'provincial_capital': '镇江', 'url': 'http://www.iecity.com/zhenjiang/map/Road---b4e5d7af--1.html', 'page': '16'},
#  {'provincial_capital': '苏州', 'url': 'http://www.iecity.com/suzhou/map/Road---b4e5d7af--1.html', 'page': '67'},
#  {'provincial_capital': '南通', 'url': 'http://www.iecity.com/nantong/map/Road---b4e5d7af--1.html', 'page': '57'},
#  {'provincial_capital': '扬州', 'url': 'http://www.iecity.com/yangzhou/map/Road---b4e5d7af--1.html', 'page': '43'},
#  {'provincial_capital': '盐城', 'url': 'http://www.iecity.com/yancheng/map/Road---b4e5d7af--1.html', 'page': '43'},
#  {'provincial_capital': '徐州', 'url': 'http://www.iecity.com/xuzhou/map/Road---b4e5d7af--1.html', 'page': '33'},
#  {'provincial_capital': '连云港', 'url': 'http://www.iecity.com/lianyungang/map/Road---b4e5d7af--1.html',
#   'page': '30'},
#  {'provincial_capital': '常州', 'url': 'http://www.iecity.com/changzhou/map/Road---b4e5d7af--1.html', 'page': '38'},
#  {'provincial_capital': '泰州', 'url': 'http://www.iecity.com/taizhou/map/Road---b4e5d7af--1.html', 'page': '18'},
#  {'provincial_capital': '宿迁', 'url': 'http://www.iecity.com/suqian/map/Road---b4e5d7af--1.html', 'page': '30'},
#  {'provincial_capital': '淮安', 'url': 'http://www.iecity.com/huaian/map/Road---b4e5d7af--1.html', 'page': '34'},
#  {'provincial_capital': '南昌', 'url': 'http://www.iecity.com/nanchang/map/Road---b4e5d7af--1.html', 'page': '47'},
#  {'provincial_capital': '九江', 'url': 'http://www.iecity.com/jiujiang/map/Road---b4e5d7af--1.html', 'page': '36'},
#  {'provincial_capital': '景德镇', 'url': 'http://www.iecity.com/jingdezhen/map/Road---b4e5d7af--1.html',
#   'page': '12'},
#  {'provincial_capital': '吉安', 'url': 'http://www.iecity.com/jian/map/Road---b4e5d7af--1.html', 'page': '38'},
#  {'provincial_capital': '宜春', 'url': 'http://www.iecity.com/yiichun/map/Road---b4e5d7af--1.html', 'page': '43'},
#  {'provincial_capital': '抚州', 'url': 'http://www.iecity.com/fuuzhou/map/Road---b4e5d7af--1.html', 'page': '35'},
#  {'provincial_capital': '新余', 'url': 'http://www.iecity.com/xinyu/map/Road---b4e5d7af--1.html', 'page': '17'},
#  {'provincial_capital': '萍乡', 'url': 'http://www.iecity.com/pingxiang/map/Road---b4e5d7af--1.html', 'page': '23'},
#  {'provincial_capital': '赣州', 'url': 'http://www.iecity.com/ganzhou/map/Road---b4e5d7af--1.html', 'page': '73'},
#  {'provincial_capital': '鹰潭', 'url': 'http://www.iecity.com/yingtan/map/Road---b4e5d7af--1.html', 'page': '17'},
#  {'provincial_capital': '上饶', 'url': 'http://www.iecity.com/shangrao/map/Road---b4e5d7af--1.html', 'page': '37'},
#  {'provincial_capital': '沈阳', 'url': 'http://www.iecity.com/shenyang/map/Road---b4e5d7af--1.html', 'page': '27'},
#  {'provincial_capital': '大连', 'url': 'http://www.iecity.com/dalian/map/Road---b4e5d7af--1.html', 'page': '45'},
#  {'provincial_capital': '鞍山', 'url': 'http://www.iecity.com/anshan/map/Road---b4e5d7af--1.html', 'page': '27'},
#  {'provincial_capital': '抚顺', 'url': 'http://www.iecity.com/fushun/map/Road---b4e5d7af--1.html', 'page': '18'},
#  {'provincial_capital': '本溪', 'url': 'http://www.iecity.com/benxi/map/Road---b4e5d7af--1.html', 'page': '19'},
#  {'provincial_capital': '丹东', 'url': 'http://www.iecity.com/dandong/map/Road---b4e5d7af--1.html', 'page': '40'},
#  {'provincial_capital': '锦州', 'url': 'http://www.iecity.com/jinzhou/map/Road---b4e5d7af--1.html', 'page': '32'},
#  {'provincial_capital': '营口', 'url': 'http://www.iecity.com/yingkou/map/Road---b4e5d7af--1.html', 'page': '13'},
#  {'provincial_capital': '辽阳', 'url': 'http://www.iecity.com/liaoyang/map/Road---b4e5d7af--1.html', 'page': '12'},
#  {'provincial_capital': '盘锦', 'url': 'http://www.iecity.com/panjin/map/Road---b4e5d7af--1.html', 'page': '12'},
#  {'provincial_capital': '葫芦岛', 'url': 'http://www.iecity.com/huludao/map/Road---b4e5d7af--1.html', 'page': '25'},
#  {'provincial_capital': '朝阳', 'url': 'http://www.iecity.com/chaoyang/map/Road---b4e5d7af--1.html', 'page': '32'},
#  {'provincial_capital': '铁岭', 'url': 'http://www.iecity.com/tieling/map/Road---b4e5d7af--1.html', 'page': '28'},
#  {'provincial_capital': '阜新', 'url': 'http://www.iecity.com/fuxin/map/Road---b4e5d7af--1.html', 'page': '16'},
#  {'provincial_capital': '呼和浩特', 'url': 'http://www.iecity.com/huhehaote/map/Road---b4e5d7af--1.html',
#   'page': '26'},
#  {'provincial_capital': '包头', 'url': 'http://www.iecity.com/baotou/map/Road---b4e5d7af--1.html', 'page': '17'},
#  {'provincial_capital': '乌兰察布', 'url': 'http://www.iecity.com/wulanchabu/map/Road---b4e5d7af--1.html',
#   'page': '28'},
#  {'provincial_capital': '乌海', 'url': 'http://www.iecity.com/wuhai/map/Road---b4e5d7af--1.html', 'page': '3'},
#  {'provincial_capital': '兴安盟', 'url': 'http://www.iecity.com/xinganmeng/map/Road---b4e5d7af--1.html',
#   'page': '14'},
#  {'provincial_capital': '呼伦贝尔', 'url': 'http://www.iecity.com/hulunbeier/map/Road---b4e5d7af--1.html',
#   'page': '14'},
#  {'provincial_capital': '赤峰', 'url': 'http://www.iecity.com/chifeng/map/Road---b4e5d7af--1.html', 'page': '32'},
#  {'provincial_capital': '通辽', 'url': 'http://www.iecity.com/tongliao/map/Road---b4e5d7af--1.html', 'page': '24'},
#  {'provincial_capital': '鄂尔多斯', 'url': 'http://www.iecity.com/eerduosi/map/Road---b4e5d7af--1.html', 'page': '33'},
#  {'provincial_capital': '阿拉善盟', 'url': 'http://www.iecity.com/alashan/map/Road---b4e5d7af--1.html', 'page': '14'},
#  {'provincial_capital': '巴彦淖尔盟', 'url': 'http://www.iecity.com/bayannaoer/map/Road---b4e5d7af--1.html',
#   'page': '11'},
#  {'provincial_capital': '锡林郭勒盟', 'url': 'http://www.iecity.com/xilinguole/map/Road---b4e5d7af--1.html',
#   'page': '15'},
#  {'provincial_capital': '银川', 'url': 'http://www.iecity.com/yinchuan/map/Road---b4e5d7af--1.html', 'page': '12'},
#  {'provincial_capital': '中卫', 'url': 'http://www.iecity.com/zhongwei/map/Road---b4e5d7af--1.html', 'page': '11'},
#  {'provincial_capital': '吴忠', 'url': 'http://www.iecity.com/wuzhong/map/Road---b4e5d7af--1.html', 'page': '14'},
#  {'provincial_capital': '石嘴山', 'url': 'http://www.iecity.com/shizuishan/map/Road---b4e5d7af--1.html',
#   'page': '12'},
#  {'provincial_capital': '固原', 'url': 'http://www.iecity.com/guyuan/map/Road---b4e5d7af--1.html', 'page': '18'},
#  {'provincial_capital': '西宁', 'url': 'http://www.iecity.com/xining/map/Road---b4e5d7af--1.html', 'page': '11'},
#  {'provincial_capital': '海东地区', 'url': 'http://www.iecity.com/haidong/map/Road---b4e5d7af--1.html', 'page': '5'},
#  {'provincial_capital': '海北州', 'url': 'http://www.iecity.com/haibei/map/Road---b4e5d7af--1.html', 'page': '10'},
#  {'provincial_capital': '海南州', 'url': 'http://www.iecity.com/hainan/map/Road---b4e5d7af--1.html', 'page': '11'},
#  {'provincial_capital': '果洛州', 'url': 'http://www.iecity.com/guoluo/map/Road---b4e5d7af--1.html', 'page': '7'},
#  {'provincial_capital': '黄南州', 'url': 'http://www.iecity.com/huangnan/map/Road---b4e5d7af--1.html', 'page': '7'},
#  {'provincial_capital': '玉树州', 'url': 'http://www.iecity.com/yushu/map/Road---b4e5d7af--1.html', 'page': '9'},
#  {'provincial_capital': '海西州', 'url': 'http://www.iecity.com/haixi/map/Road---b4e5d7af--1.html', 'page': '8'},
#  {'provincial_capital': '太原', 'url': 'http://www.iecity.com/taiyuan/map/Road---b4e5d7af--1.html', 'page': '19'},
#  {'provincial_capital': '临汾', 'url': 'http://www.iecity.com/linfen/map/Road---b4e5d7af--1.html', 'page': '32'},
#  {'provincial_capital': '吕梁', 'url': 'http://www.iecity.com/lvliang/map/Road---b4e5d7af--1.html', 'page': '33'},
#  {'provincial_capital': '大同', 'url': 'http://www.iecity.com/datong/map/Road---b4e5d7af--1.html', 'page': '15'},
#  {'provincial_capital': '忻州', 'url': 'http://www.iecity.com/xinzhou/map/Road---b4e5d7af--1.html', 'page': '22'},
#  {'provincial_capital': '晋中', 'url': 'http://www.iecity.com/jinzhong/map/Road---b4e5d7af--1.html', 'page': '30'},
#  {'provincial_capital': '晋城', 'url': 'http://www.iecity.com/jincheng/map/Road---b4e5d7af--1.html', 'page': '31'},
#  {'provincial_capital': '朔州', 'url': 'http://www.iecity.com/shuozhou/map/Road---b4e5d7af--1.html', 'page': '12'},
#  {'provincial_capital': '运城', 'url': 'http://www.iecity.com/yuncheng/map/Road---b4e5d7af--1.html', 'page': '30'},
#  {'provincial_capital': '长治', 'url': 'http://www.iecity.com/changzhi/map/Road---b4e5d7af--1.html', 'page': '41'},
#  {'provincial_capital': '阳泉', 'url': 'http://www.iecity.com/yangquan/map/Road---b4e5d7af--1.html', 'page': '13'},
#  {'provincial_capital': '济南', 'url': 'http://www.iecity.com/jinan/map/Road---b4e5d7af--1.html', 'page': '57'},
#  {'provincial_capital': '青岛', 'url': 'http://www.iecity.com/qingdao/map/Road---b4e5d7af--1.html', 'page': '37'},
#  {'provincial_capital': '淄博', 'url': 'http://www.iecity.com/zibo/map/Road---b4e5d7af--1.html', 'page': '22'},
#  {'provincial_capital': '德州', 'url': 'http://www.iecity.com/dezhou/map/Road---b4e5d7af--1.html', 'page': '33'},
#  {'provincial_capital': '烟台', 'url': 'http://www.iecity.com/yantai/map/Road---b4e5d7af--1.html', 'page': '30'},
#  {'provincial_capital': '潍坊', 'url': 'http://www.iecity.com/weifang/map/Road---b4e5d7af--1.html', 'page': '42'},
#  {'provincial_capital': '泰安', 'url': 'http://www.iecity.com/taian/map/Road---b4e5d7af--1.html', 'page': '32'},
#  {'provincial_capital': '东营', 'url': 'http://www.iecity.com/dongying/map/Road---b4e5d7af--1.html', 'page': '19'},
#  {'provincial_capital': '威海', 'url': 'http://www.iecity.com/weihai/map/Road---b4e5d7af--1.html', 'page': '16'},
#  {'provincial_capital': '临沂', 'url': 'http://www.iecity.com/linyi/map/Road---b4e5d7af--1.html', 'page': '42'},
#  {'provincial_capital': '日照', 'url': 'http://www.iecity.com/rizhao/map/Road---b4e5d7af--1.html', 'page': '22'},
#  {'provincial_capital': '枣庄', 'url': 'http://www.iecity.com/zaozhuang/map/Road---b4e5d7af--1.html', 'page': '21'},
#  {'provincial_capital': '济宁', 'url': 'http://www.iecity.com/jining/map/Road---b4e5d7af--1.html', 'page': '34'},
#  {'provincial_capital': '滨州', 'url': 'http://www.iecity.com/binzhou/map/Road---b4e5d7af--1.html', 'page': '31'},
#  {'provincial_capital': '聊城', 'url': 'http://www.iecity.com/liaocheng/map/Road---b4e5d7af--1.html', 'page': '34'},
#  {'provincial_capital': '莱芜', 'url': 'http://www.iecity.com/laiwu/map/Road---b4e5d7af--1.html', 'page': '0'},
#  {'provincial_capital': '菏泽', 'url': 'http://www.iecity.com/heze/map/Road---b4e5d7af--1.html', 'page': '42'},
#  {'provincial_capital': '西安', 'url': 'http://www.iecity.com/xian/map/Road---b4e5d7af--1.html', 'page': '51'},
#  {'provincial_capital': '咸阳', 'url': 'http://www.iecity.com/xianyang/map/Road---b4e5d7af--1.html', 'page': '24'},
#  {'provincial_capital': '延安', 'url': 'http://www.iecity.com/yanan/map/Road---b4e5d7af--1.html', 'page': '30'},
#  {'provincial_capital': '宝鸡', 'url': 'http://www.iecity.com/baoji/map/Road---b4e5d7af--1.html', 'page': '43'},
#  {'provincial_capital': '商洛', 'url': 'http://www.iecity.com/shangluo/map/Road---b4e5d7af--1.html', 'page': '28'},
#  {'provincial_capital': '安康', 'url': 'http://www.iecity.com/ankang/map/Road---b4e5d7af--1.html', 'page': '46'},
#  {'provincial_capital': '榆林', 'url': 'http://www.iecity.com/yuulin/map/Road---b4e5d7af--1.html', 'page': '52'},
#  {'provincial_capital': '汉中', 'url': 'http://www.iecity.com/hanzhong/map/Road---b4e5d7af--1.html', 'page': '70'},
#  {'provincial_capital': '渭南', 'url': 'http://www.iecity.com/weinan/map/Road---b4e5d7af--1.html', 'page': '33'},
#  {'provincial_capital': '铜川', 'url': 'http://www.iecity.com/tongchuan/map/Road---b4e5d7af--1.html', 'page': '16'},
#  {'provincial_capital': '成都', 'url': 'http://www.iecity.com/chengdu/map/Road---b4e5d7af--1.html', 'page': '79'},
#  {'provincial_capital': '自贡', 'url': 'http://www.iecity.com/zigong/map/Road---b4e5d7af--1.html', 'page': '21'},
#  {'provincial_capital': '绵阳', 'url': 'http://www.iecity.com/mianyang/map/Road---b4e5d7af--1.html', 'page': '53'},
#  {'provincial_capital': '泸州', 'url': 'http://www.iecity.com/luzhou/map/Road---b4e5d7af--1.html', 'page': '56'},
#  {'provincial_capital': '宜宾', 'url': 'http://www.iecity.com/yibin/map/Road---b4e5d7af--1.html', 'page': '48'},
#  {'provincial_capital': '内江', 'url': 'http://www.iecity.com/neijiang/map/Road---b4e5d7af--1.html', 'page': '22'},
#  {'provincial_capital': '资阳', 'url': 'http://www.iecity.com/ziyang/map/Road---b4e5d7af--1.html', 'page': '26'},
#  {'provincial_capital': '乐山', 'url': 'http://www.iecity.com/leshan/map/Road---b4e5d7af--1.html', 'page': '39'},
#  {'provincial_capital': '眉山', 'url': 'http://www.iecity.com/meishan/map/Road---b4e5d7af--1.html', 'page': '14'},
#  {'provincial_capital': '凉山', 'url': 'http://www.iecity.com/liangshan/map/Road---b4e5d7af--1.html', 'page': '47'},
#  {'provincial_capital': '南充', 'url': 'http://www.iecity.com/nanchong/map/Road---b4e5d7af--1.html', 'page': '40'},
#  {'provincial_capital': '巴中', 'url': 'http://www.iecity.com/bazhong/map/Road---b4e5d7af--1.html', 'page': '50'},
#  {'provincial_capital': '广元', 'url': 'http://www.iecity.com/guangyuan/map/Road---b4e5d7af--1.html', 'page': '59'},
#  {'provincial_capital': '广安', 'url': 'http://www.iecity.com/guangan/map/Road---b4e5d7af--1.html', 'page': '23'},
#  {'provincial_capital': '德阳', 'url': 'http://www.iecity.com/deyang/map/Road---b4e5d7af--1.html', 'page': '32'},
#  {'provincial_capital': '攀枝花', 'url': 'http://www.iecity.com/panzhihua/map/Road---b4e5d7af--1.html', 'page': '19'},
#  {'provincial_capital': '甘孜', 'url': 'http://www.iecity.com/ganzi/map/Road---b4e5d7af--1.html', 'page': '25'},
#  {'provincial_capital': '达州', 'url': 'http://www.iecity.com/dazhou/map/Road---b4e5d7af--1.html', 'page': '47'},
#  {'provincial_capital': '遂宁', 'url': 'http://www.iecity.com/suining/map/Road---b4e5d7af--1.html', 'page': '22'},
#  {'provincial_capital': '阿坝', 'url': 'http://www.iecity.com/aba/map/Road---b4e5d7af--1.html', 'page': '22'},
#  {'provincial_capital': '雅安', 'url': 'http://www.iecity.com/yaan/map/Road---b4e5d7af--1.html', 'page': '20'},
#  {'provincial_capital': '乌鲁木齐', 'url': 'http://www.iecity.com/wulumuqi/map/Road---b4e5d7af--1.html', 'page': '13'},
#  {'provincial_capital': '伊犁州', 'url': 'http://www.iecity.com/yili/map/Road---b4e5d7af--1.html', 'page': '15'},
#  {'provincial_capital': '克拉玛依', 'url': 'http://www.iecity.com/kelamayi/map/Road---b4e5d7af--1.html', 'page': '1'},
#  {'provincial_capital': '博尔塔拉', 'url': 'http://www.iecity.com/boertala/map/Road---b4e5d7af--1.html', 'page': '7'},
#  {'provincial_capital': '吐鲁番', 'url': 'http://www.iecity.com/tulufan/map/Road---b4e5d7af--1.html', 'page': '4'},
#  {'provincial_capital': '塔城', 'url': 'http://www.iecity.com/tacheng/map/Road---b4e5d7af--1.html', 'page': '15'},
#  {'provincial_capital': '昌吉', 'url': 'http://www.iecity.com/changji/map/Road---b4e5d7af--1.html', 'page': '13'},
#  {'provincial_capital': '石河子', 'url': 'http://www.iecity.com/shihezi/map/Road---b4e5d7af--1.html', 'page': '2'},
#  {'provincial_capital': '阿克苏', 'url': 'http://www.iecity.com/akesu/map/Road---b4e5d7af--1.html', 'page': '21'},
#  {'provincial_capital': '阿勒泰', 'url': 'http://www.iecity.com/aletai/map/Road---b4e5d7af--1.html', 'page': '18'},
#  {'provincial_capital': '巴音郭楞', 'url': 'http://www.iecity.com/bayinguoleng/map/Road---b4e5d7af--1.html',
#   'page': '16'},
#  {'provincial_capital': '哈密地区', 'url': 'http://www.iecity.com/hami/map/Road---b4e5d7af--1.html', 'page': '9'},
#  {'provincial_capital': '和田地区', 'url': 'http://www.iecity.com/hetian/map/Road---b4e5d7af--1.html', 'page': '16'},
#  {'provincial_capital': '喀什地区', 'url': 'http://www.iecity.com/kashi/map/Road---b4e5d7af--1.html', 'page': '31'},
#  {'provincial_capital': '克孜勒苏', 'url': 'http://www.iecity.com/kezilesu/map/Road---b4e5d7af--1.html', 'page': '13'},
#  {'provincial_capital': '北屯', 'url': 'http://www.iecity.com/beitun/map/Road---b4e5d7af--1.html', 'page': '0'},
#  {'provincial_capital': '铁门关', 'url': 'http://www.iecity.com/tiemenguan/map/Road---b4e5d7af--1.html', 'page': '0'},
#  {'provincial_capital': '双河', 'url': 'http://www.iecity.com/shuanghe/map/Road---b4e5d7af--1.html', 'page': '1'},
#  {'provincial_capital': '可克达拉', 'url': 'http://www.iecity.com/kekedala/map/Road---b4e5d7af--1.html', 'page': '1'},
#  {'provincial_capital': '昆玉', 'url': 'http://www.iecity.com/kunyu/map/Road---b4e5d7af--1.html', 'page': '1'},
#  {'provincial_capital': '五家渠', 'url': 'http://www.iecity.com/wujiaju/map/Road---b4e5d7af--1.html', 'page': '1'},
#  {'provincial_capital': '阿拉尔', 'url': 'http://www.iecity.com/alaer/map/Road---b4e5d7af--1.html', 'page': '0'},
#  {'provincial_capital': '图木舒克', 'url': 'http://www.iecity.com/tumushuke/map/Road---b4e5d7af--1.html', 'page': '0'},
#  {'provincial_capital': '香港', 'url': 'http://www.iecity.com/xianggang/map/Road---b4e5d7af--1.html', 'page': '16'},
#  {'provincial_capital': '拉萨', 'url': 'http://www.iecity.com/lasa/map/Road---b4e5d7af--1.html', 'page': '16'},
#  {'provincial_capital': '山南地区', 'url': 'http://www.iecity.com/shannan/map/Road---b4e5d7af--1.html', 'page': '14'},
#  {'provincial_capital': '日喀则', 'url': 'http://www.iecity.com/rikaze/map/Road---b4e5d7af--1.html', 'page': '21'},
#  {'provincial_capital': '阿里地区', 'url': 'http://www.iecity.com/ali/map/Road---b4e5d7af--1.html', 'page': '10'},
#  {'provincial_capital': '昌都地区', 'url': 'http://www.iecity.com/changdu/map/Road---b4e5d7af--1.html', 'page': '20'},
#  {'provincial_capital': '林芝地区', 'url': 'http://www.iecity.com/linzhi/map/Road---b4e5d7af--1.html', 'page': '12'},
#  {'provincial_capital': '那曲地区', 'url': 'http://www.iecity.com/naqu/map/Road---b4e5d7af--1.html', 'page': '14'},
#  {'provincial_capital': '昆明', 'url': 'http://www.iecity.com/kunming/map/Road---b4e5d7af--1.html', 'page': '39'},
#  {'provincial_capital': '玉溪', 'url': 'http://www.iecity.com/yuxi/map/Road---b4e5d7af--1.html', 'page': '21'},
#  {'provincial_capital': '大理', 'url': 'http://www.iecity.com/dali/map/Road---b4e5d7af--1.html', 'page': '34'},
#  {'provincial_capital': '昭通', 'url': 'http://www.iecity.com/zhaotong/map/Road---b4e5d7af--1.html', 'page': '37'},
#  {'provincial_capital': '曲靖', 'url': 'http://www.iecity.com/qujing/map/Road---b4e5d7af--1.html', 'page': '43'},
#  {'provincial_capital': '楚雄', 'url': 'http://www.iecity.com/chuxiong/map/Road---b4e5d7af--1.html', 'page': '33'},
#  {'provincial_capital': '红河', 'url': 'http://www.iecity.com/honghe/map/Road---b4e5d7af--1.html', 'page': '27'},
#  {'provincial_capital': '西双版纳', 'url': 'http://www.iecity.com/xishuangbanna/map/Road---b4e5d7af--1.html',
#   'page': '12'},
#  {'provincial_capital': '保山', 'url': 'http://www.iecity.com/baoshan/map/Road---b4e5d7af--1.html', 'page': '25'},
#  {'provincial_capital': '德宏州', 'url': 'http://www.iecity.com/dehong/map/Road---b4e5d7af--1.html', 'page': '15'},
#  {'provincial_capital': '迪庆州', 'url': 'http://www.iecity.com/diqing/map/Road---b4e5d7af--1.html', 'page': '11'},
#  {'provincial_capital': '丽江', 'url': 'http://www.iecity.com/lijiang/map/Road---b4e5d7af--1.html', 'page': '17'},
#  {'provincial_capital': '临沧地区', 'url': 'http://www.iecity.com/lincang/map/Road---b4e5d7af--1.html', 'page': '12'},
#  {'provincial_capital': '怒江州', 'url': 'http://www.iecity.com/nujiang/map/Road---b4e5d7af--1.html', 'page': '13'},
#  {'provincial_capital': '普洱', 'url': 'http://www.iecity.com/puer/map/Road---b4e5d7af--1.html', 'page': '27'},
#  {'provincial_capital': '文山州', 'url': 'http://www.iecity.com/wenshan/map/Road---b4e5d7af--1.html', 'page': '31'},
#  {'provincial_capital': '杭州', 'url': 'http://www.iecity.com/hangzhou/map/Road---b4e5d7af--1.html', 'page': '74'},
#  {'provincial_capital': '嘉兴', 'url': 'http://www.iecity.com/jiaxing/map/Road---b4e5d7af--1.html', 'page': '77'},
#  {'provincial_capital': '绍兴', 'url': 'http://www.iecity.com/shaoxing/map/Road---b4e5d7af--1.html', 'page': '37'},
#  {'provincial_capital': '湖州', 'url': 'http://www.iecity.com/huzhou/map/Road---b4e5d7af--1.html', 'page': '32'},
#  {'provincial_capital': '宁波', 'url': 'http://www.iecity.com/ningbo/map/Road---b4e5d7af--1.html', 'page': '69'},
#  {'provincial_capital': '台州', 'url': 'http://www.iecity.com/taiizhou/map/Road---b4e5d7af--1.html', 'page': '31'},
#  {'provincial_capital': '温州', 'url': 'http://www.iecity.com/wenzhou/map/Road---b4e5d7af--1.html', 'page': '44'},
#  {'provincial_capital': '金华', 'url': 'http://www.iecity.com/jinhua/map/Road---b4e5d7af--1.html', 'page': '37'},
#  {'provincial_capital': '舟山', 'url': 'http://www.iecity.com/zhoushan/map/Road---b4e5d7af--1.html', 'page': '30'},
#  {'provincial_capital': '丽水', 'url': 'http://www.iecity.com/lishui/map/Road---b4e5d7af--1.html', 'page': '37'},
#  {'provincial_capital': '衢州', 'url': 'http://www.iecity.com/quzhou/map/Road---b4e5d7af--1.html', 'page': '36'}]