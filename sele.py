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

    city_href = html.xpath('//*[@class="CityList"]//a/@href')
    count = 0
    city_list = []
    for city,city_href, in zip(city,city_href):
        item = {}
        city_href = re.findall(r'http://www.iecity.com/(.*?)/map/', city_href)[0]
        city_href = 'http://www.iecity.com/'+city_href+'/map/Road---b4e5d7af--1.html'
        res = requests.get(city_href,headers=headers)
        res.encoding = res.apparent_encoding
        res = res.text
        try:
            pages = re.findall(r'当前在第 .* 页 共计 (.*?) 个页面 共有 .* 条记录', res)[0]
            # print(city_href, pages)
        except:
            item['page'] = '0'
        else:
            item['provincial_capital'] = city
            item['link'] = city_href
            item['page'] = pages
            count += 1
            city_list.append(item)
            print(count,item)
    print(city_list)
    # city_html = 'http://www.iecity.com/kelamayi/map/Road---b4e5d7af--1.html'

    # [{'provincial_capital': '澳门', 'link': 'http://www.iecity.com/aomen/map/Road---b4e5d7af--1.html', 'page': '1'},
    #  {'provincial_capital': '合肥', 'link': 'http://www.iecity.com/hefei/map/Road---b4e5d7af--1.html', 'page': '73'},
    #  {'provincial_capital': '蚌埠', 'link': 'http://www.iecity.com/bangbu/map/Road---b4e5d7af--1.html', 'page': '24'},
    #  {'provincial_capital': '芜湖', 'link': 'http://www.iecity.com/wuhu/map/Road---b4e5d7af--1.html', 'page': '37'},
    #  {'provincial_capital': '马鞍山', 'link': 'http://www.iecity.com/maanshan/map/Road---b4e5d7af--1.html', 'page': '23'},
    #  {'provincial_capital': '安庆', 'link': 'http://www.iecity.com/anqing/map/Road---b4e5d7af--1.html', 'page': '50'},
    #  {'provincial_capital': '黄山', 'link': 'http://www.iecity.com/huangshan/map/Road---b4e5d7af--1.html', 'page': '37'},
    #  {'provincial_capital': '巢湖', 'link': 'http://www.iecity.com/chaohu/map/Road---b4e5d7af--1.html', 'page': '0'},
    #  {'provincial_capital': '亳州', 'link': 'http://www.iecity.com/haozhou/map/Road---b4e5d7af--1.html', 'page': '39'},
    #  {'provincial_capital': '六安', 'link': 'http://www.iecity.com/liuan/map/Road---b4e5d7af--1.html', 'page': '47'},
    #  {'provincial_capital': '宣城', 'link': 'http://www.iecity.com/xuancheng/map/Road---b4e5d7af--1.html', 'page': '29'},
    #  {'provincial_capital': '宿州', 'link': 'http://www.iecity.com/suuzhou/map/Road---b4e5d7af--1.html', 'page': '40'},
    #  {'provincial_capital': '池州', 'link': 'http://www.iecity.com/chizhou/map/Road---b4e5d7af--1.html', 'page': '28'},
    #  {'provincial_capital': '淮北', 'link': 'http://www.iecity.com/huaibei/map/Road---b4e5d7af--1.html', 'page': '16'},
    #  {'provincial_capital': '淮南', 'link': 'http://www.iecity.com/huainan/map/Road---b4e5d7af--1.html', 'page': '19'},
    #  {'provincial_capital': '滁州', 'link': 'http://www.iecity.com/chuzhou/map/Road---b4e5d7af--1.html', 'page': '41'},
    #  {'provincial_capital': '铜陵', 'link': 'http://www.iecity.com/tongling/map/Road---b4e5d7af--1.html', 'page': '13'},
    #  {'provincial_capital': '阜阳', 'link': 'http://www.iecity.com/fuyang/map/Road---b4e5d7af--1.html', 'page': '39'},
    #  {'provincial_capital': '福州', 'link': 'http://www.iecity.com/fuzhou/map/Road---b4e5d7af--1.html', 'page': '46'},
    #  {'provincial_capital': '厦门', 'link': 'http://www.iecity.com/xiamen/map/Road---b4e5d7af--1.html', 'page': '23'},
    #  {'provincial_capital': '宁德', 'link': 'http://www.iecity.com/ningde/map/Road---b4e5d7af--1.html', 'page': '29'},
    #  {'provincial_capital': '莆田', 'link': 'http://www.iecity.com/putian/map/Road---b4e5d7af--1.html', 'page': '19'},
    #  {'provincial_capital': '泉州', 'link': 'http://www.iecity.com/quanzhou/map/Road---b4e5d7af--1.html', 'page': '38'},
    #  {'provincial_capital': '漳州', 'link': 'http://www.iecity.com/zhangzhou/map/Road---b4e5d7af--1.html', 'page': '26'},
    #  {'provincial_capital': '三明', 'link': 'http://www.iecity.com/sanming/map/Road---b4e5d7af--1.html', 'page': '28'},
    #  {'provincial_capital': '南平', 'link': 'http://www.iecity.com/nanping/map/Road---b4e5d7af--1.html', 'page': '26'},
    #  {'provincial_capital': '龙岩', 'link': 'http://www.iecity.com/longyan/map/Road---b4e5d7af--1.html', 'page': '23'},
    #  {'provincial_capital': '深圳', 'link': 'http://www.iecity.com/shenzhen/map/Road---b4e5d7af--1.html', 'page': '25'},
    #  {'provincial_capital': '珠海', 'link': 'http://www.iecity.com/zhuhai/map/Road---b4e5d7af--1.html', 'page': '14'},
    #  {'provincial_capital': '佛山', 'link': 'http://www.iecity.com/foshan/map/Road---b4e5d7af--1.html', 'page': '36'},
    #  {'provincial_capital': '肇庆', 'link': 'http://www.iecity.com/zhaoqing/map/Road---b4e5d7af--1.html', 'page': '38'},
    #  {'provincial_capital': '汕头', 'link': 'http://www.iecity.com/shantou/map/Road---b4e5d7af--1.html', 'page': '18'},
    #  {'provincial_capital': '湛江', 'link': 'http://www.iecity.com/zhanjiang/map/Road---b4e5d7af--1.html', 'page': '25'},
    #  {'provincial_capital': '中山', 'link': 'http://www.iecity.com/zhongshan/map/Road---b4e5d7af--1.html', 'page': '18'},
    #  {'provincial_capital': '潮州', 'link': 'http://www.iecity.com/chaozhou/map/Road---b4e5d7af--1.html', 'page': '19'},
    #  {'provincial_capital': '东莞', 'link': 'http://www.iecity.com/dongguan/map/Road---b4e5d7af--1.html', 'page': '22'},
    #  {'provincial_capital': '阳江', 'link': 'http://www.iecity.com/yangjiang/map/Road---b4e5d7af--1.html', 'page': '24'},
    #  {'provincial_capital': '揭阳', 'link': 'http://www.iecity.com/jieyang/map/Road---b4e5d7af--1.html', 'page': '18'},
    #  {'provincial_capital': '茂名', 'link': 'http://www.iecity.com/maoming/map/Road---b4e5d7af--1.html', 'page': '38'},
    #  {'provincial_capital': '江门', 'link': 'http://www.iecity.com/jiangmen/map/Road---b4e5d7af--1.html', 'page': '38'},
    #  {'provincial_capital': '韶关', 'link': 'http://www.iecity.com/shaoguan/map/Road---b4e5d7af--1.html', 'page': '37'},
    #  {'provincial_capital': '惠州', 'link': 'http://www.iecity.com/huizhou/map/Road---b4e5d7af--1.html', 'page': '45'},
    #  {'provincial_capital': '梅州', 'link': 'http://www.iecity.com/meizhou/map/Road---b4e5d7af--1.html', 'page': '56'},
    #  {'provincial_capital': '云浮', 'link': 'http://www.iecity.com/yunfu/map/Road---b4e5d7af--1.html', 'page': '32'},
    #  {'provincial_capital': '河源', 'link': 'http://www.iecity.com/heyuan/map/Road---b4e5d7af--1.html', 'page': '39'},
    #  {'provincial_capital': '清远', 'link': 'http://www.iecity.com/qingyuan/map/Road---b4e5d7af--1.html', 'page': '66'},
    #  {'provincial_capital': '南宁', 'link': 'http://www.iecity.com/nanning/map/Road---b4e5d7af--1.html', 'page': '39'},
    #  {'provincial_capital': '柳州', 'link': 'http://www.iecity.com/liuzhou/map/Road---b4e5d7af--1.html', 'page': '31'},
    #  {'provincial_capital': '桂林', 'link': 'http://www.iecity.com/guilin/map/Road---b4e5d7af--1.html', 'page': '60'},
    #  {'provincial_capital': '北海', 'link': 'http://www.iecity.com/beihai/map/Road---b4e5d7af--1.html', 'page': '13'},
    #  {'provincial_capital': '防城港', 'link': 'http://www.iecity.com/fangchenggang/map/Road---b4e5d7af--1.html',
    #   'page': '17'},
    #  {'provincial_capital': '崇左', 'link': 'http://www.iecity.com/chongzuo/map/Road---b4e5d7af--1.html', 'page': '21'},
    #  {'provincial_capital': '来宾', 'link': 'http://www.iecity.com/laibin/map/Road---b4e5d7af--1.html', 'page': '17'},
    #  {'provincial_capital': '梧州', 'link': 'http://www.iecity.com/wuzhou/map/Road---b4e5d7af--1.html', 'page': '23'},
    #  {'provincial_capital': '河池', 'link': 'http://www.iecity.com/hechi/map/Road---b4e5d7af--1.html', 'page': '57'},
    #  {'provincial_capital': '玉林', 'link': 'http://www.iecity.com/yulin/map/Road---b4e5d7af--1.html', 'page': '34'},
    #  {'provincial_capital': '贵港', 'link': 'http://www.iecity.com/guigang/map/Road---b4e5d7af--1.html', 'page': '35'},
    #  {'provincial_capital': '贺州', 'link': 'http://www.iecity.com/hezhou/map/Road---b4e5d7af--1.html', 'page': '32'},
    #  {'provincial_capital': '钦州', 'link': 'http://www.iecity.com/qinzhou/map/Road---b4e5d7af--1.html', 'page': '31'},
    #  {'provincial_capital': '百色', 'link': 'http://www.iecity.com/baise/map/Road---b4e5d7af--1.html', 'page': '26'},
    #  {'provincial_capital': '贵阳', 'link': 'http://www.iecity.com/guiyang/map/Road---b4e5d7af--1.html', 'page': '38'},
    #  {'provincial_capital': '安顺', 'link': 'http://www.iecity.com/anshun/map/Road---b4e5d7af--1.html', 'page': '33'},
    #  {'provincial_capital': '毕节地区', 'link': 'http://www.iecity.com/bijie/map/Road---b4e5d7af--1.html', 'page': '28'},
    #  {'provincial_capital': '遵义', 'link': 'http://www.iecity.com/zunyi/map/Road---b4e5d7af--1.html', 'page': '88'},
    #  {'provincial_capital': '铜仁地区', 'link': 'http://www.iecity.com/tongren/map/Road---b4e5d7af--1.html', 'page': '22'},
    #  {'provincial_capital': '黔东南', 'link': 'http://www.iecity.com/qiandongnan/map/Road---b4e5d7af--1.html',
    #   'page': '39'},
    #  {'provincial_capital': '黔南', 'link': 'http://www.iecity.com/qiannan/map/Road---b4e5d7af--1.html', 'page': '35'},
    #  {'provincial_capital': '六盘水', 'link': 'http://www.iecity.com/liupanshui/map/Road---b4e5d7af--1.html',
    #   'page': '25'},
    #  {'provincial_capital': '黔西南州', 'link': 'http://www.iecity.com/qianxinanzhou/map/Road---b4e5d7af--1.html',
    #   'page': '28'},
    #  {'provincial_capital': '兰州', 'link': 'http://www.iecity.com/lanzhou/map/Road---b4e5d7af--1.html', 'page': '46'},
    #  {'provincial_capital': '定西', 'link': 'http://www.iecity.com/dingxi/map/Road---b4e5d7af--1.html', 'page': '44'},
    #  {'provincial_capital': '平凉', 'link': 'http://www.iecity.com/pingliang/map/Road---b4e5d7af--1.html', 'page': '26'},
    #  {'provincial_capital': '庆阳', 'link': 'http://www.iecity.com/qingyang/map/Road---b4e5d7af--1.html', 'page': '47'},
    #  {'provincial_capital': '张掖', 'link': 'http://www.iecity.com/zhangye/map/Road---b4e5d7af--1.html', 'page': '26'},
    #  {'provincial_capital': '武威', 'link': 'http://www.iecity.com/wuwei/map/Road---b4e5d7af--1.html', 'page': '29'},
    #  {'provincial_capital': '白银', 'link': 'http://www.iecity.com/baiyin/map/Road---b4e5d7af--1.html', 'page': '26'},
    #  {'provincial_capital': '酒泉', 'link': 'http://www.iecity.com/jiuquan/map/Road---b4e5d7af--1.html', 'page': '15'},
    #  {'provincial_capital': '金昌', 'link': 'http://www.iecity.com/jinchang/map/Road---b4e5d7af--1.html', 'page': '10'},
    #  {'provincial_capital': '陇南', 'link': 'http://www.iecity.com/longnan/map/Road---b4e5d7af--1.html', 'page': '37'},
    #  {'provincial_capital': '临夏', 'link': 'http://www.iecity.com/linxia/map/Road---b4e5d7af--1.html', 'page': '25'},
    #  {'provincial_capital': '甘南州', 'link': 'http://www.iecity.com/gannanzhou/map/Road---b4e5d7af--1.html',
    #   'page': '18'},
    #  {'provincial_capital': '嘉峪关', 'link': 'http://www.iecity.com/jiayuguan/map/Road---b4e5d7af--1.html', 'page': '3'},
    #  {'provincial_capital': '邯郸', 'link': 'http://www.iecity.com/handan/map/Road---b4e5d7af--1.html', 'page': '42'},
    #  {'provincial_capital': '石家庄', 'link': 'http://www.iecity.com/shijiazhuang/map/Road---b4e5d7af--1.html',
    #   'page': '38'},
    #  {'provincial_capital': '保定', 'link': 'http://www.iecity.com/baoding/map/Road---b4e5d7af--1.html', 'page': '58'},
    #  {'provincial_capital': '张家口', 'link': 'http://www.iecity.com/zhangjiakou/map/Road---b4e5d7af--1.html',
    #   'page': '30'},
    #  {'provincial_capital': '承德', 'link': 'http://www.iecity.com/chengde/map/Road---b4e5d7af--1.html', 'page': '58'},
    #  {'provincial_capital': '唐山', 'link': 'http://www.iecity.com/tangshan/map/Road---b4e5d7af--1.html', 'page': '33'},
    #  {'provincial_capital': '廊坊', 'link': 'http://www.iecity.com/langfang/map/Road---b4e5d7af--1.html', 'page': '19'},
    #  {'provincial_capital': '秦皇岛', 'link': 'http://www.iecity.com/qinhuangdao/map/Road---b4e5d7af--1.html',
    #   'page': '20'},
    #  {'provincial_capital': '沧州', 'link': 'http://www.iecity.com/cangzhou/map/Road---b4e5d7af--1.html', 'page': '29'},
    #  {'provincial_capital': '衡水', 'link': 'http://www.iecity.com/hengshui/map/Road---b4e5d7af--1.html', 'page': '39'},
    #  {'provincial_capital': '邢台', 'link': 'http://www.iecity.com/xingtai/map/Road---b4e5d7af--1.html', 'page': '34'},
    #  {'provincial_capital': '郑州', 'link': 'http://www.iecity.com/zhengzhou/map/Road---b4e5d7af--1.html', 'page': '36'},
    #  {'provincial_capital': '安阳', 'link': 'http://www.iecity.com/anyang/map/Road---b4e5d7af--1.html', 'page': '25'},
    #  {'provincial_capital': '新乡', 'link': 'http://www.iecity.com/xinxiang/map/Road---b4e5d7af--1.html', 'page': '24'},
    #  {'provincial_capital': '许昌', 'link': 'http://www.iecity.com/xuchang/map/Road---b4e5d7af--1.html', 'page': '22'},
    #  {'provincial_capital': '平顶山', 'link': 'http://www.iecity.com/pingdingshan/map/Road---b4e5d7af--1.html',
    #   'page': '25'},
    #  {'provincial_capital': '开封', 'link': 'http://www.iecity.com/kaifeng/map/Road---b4e5d7af--1.html', 'page': '35'},
    #  {'provincial_capital': '洛阳', 'link': 'http://www.iecity.com/luoyang/map/Road---b4e5d7af--1.html', 'page': '50'},
    #  {'provincial_capital': '焦作', 'link': 'http://www.iecity.com/jiaozuo/map/Road---b4e5d7af--1.html', 'page': '20'},
    #  {'provincial_capital': '三门峡', 'link': 'http://www.iecity.com/sanmenxia/map/Road---b4e5d7af--1.html', 'page': '28'},
    #  {'provincial_capital': '信阳', 'link': 'http://www.iecity.com/xinyang/map/Road---b4e5d7af--1.html', 'page': '44'},
    #  {'provincial_capital': '南阳', 'link': 'http://www.iecity.com/nanyang/map/Road---b4e5d7af--1.html', 'page': '50'},
    #  {'provincial_capital': '周口', 'link': 'http://www.iecity.com/zhoukou/map/Road---b4e5d7af--1.html', 'page': '29'},
    #  {'provincial_capital': '商丘', 'link': 'http://www.iecity.com/shangqiu/map/Road---b4e5d7af--1.html', 'page': '38'},
    #  {'provincial_capital': '济源', 'link': 'http://www.iecity.com/jiyuan/map/Road---b4e5d7af--1.html', 'page': '21'},
    #  {'provincial_capital': '漯河', 'link': 'http://www.iecity.com/luohe/map/Road---b4e5d7af--1.html', 'page': '18'},
    #  {'provincial_capital': '濮阳', 'link': 'http://www.iecity.com/puyang/map/Road---b4e5d7af--1.html', 'page': '26'},
    #  {'provincial_capital': '驻马店', 'link': 'http://www.iecity.com/zhumadian/map/Road---b4e5d7af--1.html', 'page': '39'},
    #  {'provincial_capital': '鹤壁', 'link': 'http://www.iecity.com/hebi/map/Road---b4e5d7af--1.html', 'page': '12'},
    #  {'provincial_capital': '武汉', 'link': 'http://www.iecity.com/wuhan/map/Road---b4e5d7af--1.html', 'page': '47'},
    #  {'provincial_capital': '襄樊', 'link': 'http://www.iecity.com/xiangfan/map/Road---b4e5d7af--1.html', 'page': '27'},
    #  {'provincial_capital': '鄂州', 'link': 'http://www.iecity.com/ezhou/map/Road---b4e5d7af--1.html', 'page': '18'},
    #  {'provincial_capital': '荆州', 'link': 'http://www.iecity.com/jingzhou/map/Road---b4e5d7af--1.html', 'page': '35'},
    #  {'provincial_capital': '宜昌', 'link': 'http://www.iecity.com/yichang/map/Road---b4e5d7af--1.html', 'page': '70'},
    #  {'provincial_capital': '十堰', 'link': 'http://www.iecity.com/shiyan/map/Road---b4e5d7af--1.html', 'page': '70'},
    #  {'provincial_capital': '荆门', 'link': 'http://www.iecity.com/jingmen/map/Road---b4e5d7af--1.html', 'page': '32'},
    #  {'provincial_capital': '仙桃', 'link': 'http://www.iecity.com/xiantao/map/Road---b4e5d7af--1.html', 'page': '14'},
    #  {'provincial_capital': '咸宁', 'link': 'http://www.iecity.com/xianning/map/Road---b4e5d7af--1.html', 'page': '25'},
    #  {'provincial_capital': '天门', 'link': 'http://www.iecity.com/tianmen/map/Road---b4e5d7af--1.html', 'page': '18'},
    #  {'provincial_capital': '孝感', 'link': 'http://www.iecity.com/xiaogan/map/Road---b4e5d7af--1.html', 'page': '32'},
    #  {'provincial_capital': '潜江', 'link': 'http://www.iecity.com/qianjiang/map/Road---b4e5d7af--1.html', 'page': '12'},
    #  {'provincial_capital': '随州', 'link': 'http://www.iecity.com/suizhou/map/Road---b4e5d7af--1.html', 'page': '39'},
    #  {'provincial_capital': '黄冈', 'link': 'http://www.iecity.com/huanggang/map/Road---b4e5d7af--1.html', 'page': '57'},
    #  {'provincial_capital': '神农架', 'link': 'http://www.iecity.com/shennongjia/map/Road---b4e5d7af--1.html',
    #   'page': '9'},
    #  {'provincial_capital': '恩施', 'link': 'http://www.iecity.com/enshi/map/Road---b4e5d7af--1.html', 'page': '48'},
    #  {'provincial_capital': '岳阳', 'link': 'http://www.iecity.com/yueyang/map/Road---b4e5d7af--1.html', 'page': '48'},
    #  {'provincial_capital': '长沙', 'link': 'http://www.iecity.com/changsha/map/Road---b4e5d7af--1.html', 'page': '65'},
    #  {'provincial_capital': '湘潭', 'link': 'http://www.iecity.com/xiangtan/map/Road---b4e5d7af--1.html', 'page': '33'},
    #  {'provincial_capital': '株洲', 'link': 'http://www.iecity.com/zhuzhou/map/Road---b4e5d7af--1.html', 'page': '71'},
    #  {'provincial_capital': '衡阳', 'link': 'http://www.iecity.com/hengyang/map/Road---b4e5d7af--1.html', 'page': '47'},
    #  {'provincial_capital': '常德', 'link': 'http://www.iecity.com/changde/map/Road---b4e5d7af--1.html', 'page': '47'},
    #  {'provincial_capital': '张家界', 'link': 'http://www.iecity.com/zhangjiajie/map/Road---b4e5d7af--1.html',
    #   'page': '21'},
    #  {'provincial_capital': '娄底', 'link': 'http://www.iecity.com/loudi/map/Road---b4e5d7af--1.html', 'page': '34'},
    #  {'provincial_capital': '怀化', 'link': 'http://www.iecity.com/huaihua/map/Road---b4e5d7af--1.html', 'page': '74'},
    #  {'provincial_capital': '永州', 'link': 'http://www.iecity.com/yongzhou/map/Road---b4e5d7af--1.html', 'page': '73'},
    #  {'provincial_capital': '益阳', 'link': 'http://www.iecity.com/yiyang/map/Road---b4e5d7af--1.html', 'page': '32'},
    #  {'provincial_capital': '邵阳', 'link': 'http://www.iecity.com/shaoyang/map/Road---b4e5d7af--1.html', 'page': '36'},
    #  {'provincial_capital': '郴州', 'link': 'http://www.iecity.com/chenzhou/map/Road---b4e5d7af--1.html', 'page': '42'},
    #  {'provincial_capital': '湘西', 'link': 'http://www.iecity.com/xiangxi/map/Road---b4e5d7af--1.html', 'page': '15'},
    #  {'provincial_capital': '哈尔滨', 'link': 'http://www.iecity.com/haerbin/map/Road---b4e5d7af--1.html', 'page': '40'},
    #  {'provincial_capital': '齐齐哈尔', 'link': 'http://www.iecity.com/qiqihaer/map/Road---b4e5d7af--1.html', 'page': '27'},
    #  {'provincial_capital': '牡丹江', 'link': 'http://www.iecity.com/mudanjiang/map/Road---b4e5d7af--1.html',
    #   'page': '17'},
    #  {'provincial_capital': '大庆', 'link': 'http://www.iecity.com/daqing/map/Road---b4e5d7af--1.html', 'page': '14'},
    #  {'provincial_capital': '佳木斯', 'link': 'http://www.iecity.com/jiamusi/map/Road---b4e5d7af--1.html', 'page': '18'},
    #  {'provincial_capital': '七台河', 'link': 'http://www.iecity.com/qitaihe/map/Road---b4e5d7af--1.html', 'page': '4'},
    #  {'provincial_capital': '伊春', 'link': 'http://www.iecity.com/yichun/map/Road---b4e5d7af--1.html', 'page': '7'},
    #  {'provincial_capital': '双鸭山', 'link': 'http://www.iecity.com/shuangyashan/map/Road---b4e5d7af--1.html',
    #   'page': '9'},
    #  {'provincial_capital': '大兴安岭', 'link': 'http://www.iecity.com/daxinganling/map/Road---b4e5d7af--1.html',
    #   'page': '3'},
    #  {'provincial_capital': '绥化', 'link': 'http://www.iecity.com/suihua/map/Road---b4e5d7af--1.html', 'page': '31'},
    #  {'provincial_capital': '鸡西', 'link': 'http://www.iecity.com/jixi/map/Road---b4e5d7af--1.html', 'page': '12'},
    #  {'provincial_capital': '鹤岗', 'link': 'http://www.iecity.com/hegang/map/Road---b4e5d7af--1.html', 'page': '9'},
    #  {'provincial_capital': '黑河', 'link': 'http://www.iecity.com/heihe/map/Road---b4e5d7af--1.html', 'page': '14'},
    #  {'provincial_capital': '海口', 'link': 'http://www.iecity.com/haikou/map/Road---b4e5d7af--1.html', 'page': '15'},
    #  {'provincial_capital': '三亚', 'link': 'http://www.iecity.com/sanya/map/Road---b4e5d7af--1.html', 'page': '11'},
    #  {'provincial_capital': '白沙', 'link': 'http://www.iecity.com/baishaxian/map/Road---b4e5d7af--1.html', 'page': '7'},
    #  {'provincial_capital': '保亭', 'link': 'http://www.iecity.com/baotingxian/map/Road---b4e5d7af--1.html', 'page': '8'},
    #  {'provincial_capital': '昌江', 'link': 'http://www.iecity.com/changjiangxian/map/Road---b4e5d7af--1.html',
    #   'page': '4'},
    #  {'provincial_capital': '澄迈', 'link': 'http://www.iecity.com/chengmaixian/map/Road---b4e5d7af--1.html',
    #   'page': '9'},
    #  {'provincial_capital': '定安', 'link': 'http://www.iecity.com/dinganxian/map/Road---b4e5d7af--1.html', 'page': '9'},
    #  {'provincial_capital': '东方', 'link': 'http://www.iecity.com/dongfang/map/Road---b4e5d7af--1.html', 'page': '5'},
    #  {'provincial_capital': '乐东', 'link': 'http://www.iecity.com/ledong/map/Road---b4e5d7af--1.html', 'page': '11'},
    #  {'provincial_capital': '临高县', 'link': 'http://www.iecity.com/lingaoxian/map/Road---b4e5d7af--1.html',
    #   'page': '14'},
    #  {'provincial_capital': '陵水', 'link': 'http://www.iecity.com/lingshui/map/Road---b4e5d7af--1.html', 'page': '8'},
    #  {'provincial_capital': '琼海', 'link': 'http://www.iecity.com/qionghai/map/Road---b4e5d7af--1.html', 'page': '14'},
    #  {'provincial_capital': '琼中', 'link': 'http://www.iecity.com/qiongzhong/map/Road---b4e5d7af--1.html', 'page': '11'},
    #  {'provincial_capital': '屯昌县', 'link': 'http://www.iecity.com/tunchangxian/map/Road---b4e5d7af--1.html',
    #   'page': '8'},
    #  {'provincial_capital': '万宁', 'link': 'http://www.iecity.com/wanning/map/Road---b4e5d7af--1.html', 'page': '9'},
    #  {'provincial_capital': '文昌', 'link': 'http://www.iecity.com/wenchang/map/Road---b4e5d7af--1.html', 'page': '14'},
    #  {'provincial_capital': '五指山', 'link': 'http://www.iecity.com/wuzhishan/map/Road---b4e5d7af--1.html', 'page': '5'},
    #  {'provincial_capital': '儋州', 'link': 'http://www.iecity.com/danzhou/map/Road---b4e5d7af--1.html', 'page': '16'},
    #  {'provincial_capital': '三沙', 'link': 'http://www.iecity.com/sansha/map/Road---b4e5d7af--1.html', 'page': '0'},
    #  {'provincial_capital': '长春', 'link': 'http://www.iecity.com/changchun/map/Road---b4e5d7af--1.html', 'page': '36'},
    #  {'provincial_capital': '吉林', 'link': 'http://www.iecity.com/jilin/map/Road---b4e5d7af--1.html', 'page': '23'},
    #  {'provincial_capital': '四平', 'link': 'http://www.iecity.com/siping/map/Road---b4e5d7af--1.html', 'page': '21'},
    #  {'provincial_capital': '延边', 'link': 'http://www.iecity.com/yanbian/map/Road---b4e5d7af--1.html', 'page': '8'},
    #  {'provincial_capital': '松原', 'link': 'http://www.iecity.com/songyuan/map/Road---b4e5d7af--1.html', 'page': '11'},
    #  {'provincial_capital': '白城', 'link': 'http://www.iecity.com/baicheng/map/Road---b4e5d7af--1.html', 'page': '17'},
    #  {'provincial_capital': '白山', 'link': 'http://www.iecity.com/baishan/map/Road---b4e5d7af--1.html', 'page': '11'},
    #  {'provincial_capital': '辽源', 'link': 'http://www.iecity.com/liaoyuan/map/Road---b4e5d7af--1.html', 'page': '17'},
    #  {'provincial_capital': '通化', 'link': 'http://www.iecity.com/tonghua/map/Road---b4e5d7af--1.html', 'page': '14'},
    #  {'provincial_capital': '南京', 'link': 'http://www.iecity.com/nanjing/map/Road---b4e5d7af--1.html', 'page': '60'},
    #  {'provincial_capital': '无锡', 'link': 'http://www.iecity.com/wuxi/map/Road---b4e5d7af--1.html', 'page': '42'},
    #  {'provincial_capital': '镇江', 'link': 'http://www.iecity.com/zhenjiang/map/Road---b4e5d7af--1.html', 'page': '16'},
    #  {'provincial_capital': '苏州', 'link': 'http://www.iecity.com/suzhou/map/Road---b4e5d7af--1.html', 'page': '67'},
    #  {'provincial_capital': '南通', 'link': 'http://www.iecity.com/nantong/map/Road---b4e5d7af--1.html', 'page': '57'},
    #  {'provincial_capital': '扬州', 'link': 'http://www.iecity.com/yangzhou/map/Road---b4e5d7af--1.html', 'page': '43'},
    #  {'provincial_capital': '盐城', 'link': 'http://www.iecity.com/yancheng/map/Road---b4e5d7af--1.html', 'page': '43'},
    #  {'provincial_capital': '徐州', 'link': 'http://www.iecity.com/xuzhou/map/Road---b4e5d7af--1.html', 'page': '33'},
    #  {'provincial_capital': '连云港', 'link': 'http://www.iecity.com/lianyungang/map/Road---b4e5d7af--1.html',
    #   'page': '30'},
    #  {'provincial_capital': '常州', 'link': 'http://www.iecity.com/changzhou/map/Road---b4e5d7af--1.html', 'page': '38'},
    #  {'provincial_capital': '泰州', 'link': 'http://www.iecity.com/taizhou/map/Road---b4e5d7af--1.html', 'page': '18'},
    #  {'provincial_capital': '宿迁', 'link': 'http://www.iecity.com/suqian/map/Road---b4e5d7af--1.html', 'page': '30'},
    #  {'provincial_capital': '淮安', 'link': 'http://www.iecity.com/huaian/map/Road---b4e5d7af--1.html', 'page': '34'},
    #  {'provincial_capital': '南昌', 'link': 'http://www.iecity.com/nanchang/map/Road---b4e5d7af--1.html', 'page': '47'},
    #  {'provincial_capital': '九江', 'link': 'http://www.iecity.com/jiujiang/map/Road---b4e5d7af--1.html', 'page': '36'},
    #  {'provincial_capital': '景德镇', 'link': 'http://www.iecity.com/jingdezhen/map/Road---b4e5d7af--1.html',
    #   'page': '12'},
    #  {'provincial_capital': '吉安', 'link': 'http://www.iecity.com/jian/map/Road---b4e5d7af--1.html', 'page': '38'},
    #  {'provincial_capital': '宜春', 'link': 'http://www.iecity.com/yiichun/map/Road---b4e5d7af--1.html', 'page': '43'},
    #  {'provincial_capital': '抚州', 'link': 'http://www.iecity.com/fuuzhou/map/Road---b4e5d7af--1.html', 'page': '35'},
    #  {'provincial_capital': '新余', 'link': 'http://www.iecity.com/xinyu/map/Road---b4e5d7af--1.html', 'page': '17'},
    #  {'provincial_capital': '萍乡', 'link': 'http://www.iecity.com/pingxiang/map/Road---b4e5d7af--1.html', 'page': '23'},
    #  {'provincial_capital': '赣州', 'link': 'http://www.iecity.com/ganzhou/map/Road---b4e5d7af--1.html', 'page': '73'},
    #  {'provincial_capital': '鹰潭', 'link': 'http://www.iecity.com/yingtan/map/Road---b4e5d7af--1.html', 'page': '17'},
    #  {'provincial_capital': '上饶', 'link': 'http://www.iecity.com/shangrao/map/Road---b4e5d7af--1.html', 'page': '37'},
    #  {'provincial_capital': '沈阳', 'link': 'http://www.iecity.com/shenyang/map/Road---b4e5d7af--1.html', 'page': '27'},
    #  {'provincial_capital': '大连', 'link': 'http://www.iecity.com/dalian/map/Road---b4e5d7af--1.html', 'page': '45'},
    #  {'provincial_capital': '鞍山', 'link': 'http://www.iecity.com/anshan/map/Road---b4e5d7af--1.html', 'page': '27'},
    #  {'provincial_capital': '抚顺', 'link': 'http://www.iecity.com/fushun/map/Road---b4e5d7af--1.html', 'page': '18'},
    #  {'provincial_capital': '本溪', 'link': 'http://www.iecity.com/benxi/map/Road---b4e5d7af--1.html', 'page': '19'},
    #  {'provincial_capital': '丹东', 'link': 'http://www.iecity.com/dandong/map/Road---b4e5d7af--1.html', 'page': '40'},
    #  {'provincial_capital': '锦州', 'link': 'http://www.iecity.com/jinzhou/map/Road---b4e5d7af--1.html', 'page': '32'},
    #  {'provincial_capital': '营口', 'link': 'http://www.iecity.com/yingkou/map/Road---b4e5d7af--1.html', 'page': '13'},
    #  {'provincial_capital': '辽阳', 'link': 'http://www.iecity.com/liaoyang/map/Road---b4e5d7af--1.html', 'page': '12'},
    #  {'provincial_capital': '盘锦', 'link': 'http://www.iecity.com/panjin/map/Road---b4e5d7af--1.html', 'page': '12'},
    #  {'provincial_capital': '葫芦岛', 'link': 'http://www.iecity.com/huludao/map/Road---b4e5d7af--1.html', 'page': '25'},
    #  {'provincial_capital': '朝阳', 'link': 'http://www.iecity.com/chaoyang/map/Road---b4e5d7af--1.html', 'page': '32'},
    #  {'provincial_capital': '铁岭', 'link': 'http://www.iecity.com/tieling/map/Road---b4e5d7af--1.html', 'page': '28'},
    #  {'provincial_capital': '阜新', 'link': 'http://www.iecity.com/fuxin/map/Road---b4e5d7af--1.html', 'page': '16'},
    #  {'provincial_capital': '呼和浩特', 'link': 'http://www.iecity.com/huhehaote/map/Road---b4e5d7af--1.html',
    #   'page': '26'},
    #  {'provincial_capital': '包头', 'link': 'http://www.iecity.com/baotou/map/Road---b4e5d7af--1.html', 'page': '17'},
    #  {'provincial_capital': '乌兰察布', 'link': 'http://www.iecity.com/wulanchabu/map/Road---b4e5d7af--1.html',
    #   'page': '28'},
    #  {'provincial_capital': '乌海', 'link': 'http://www.iecity.com/wuhai/map/Road---b4e5d7af--1.html', 'page': '3'},
    #  {'provincial_capital': '兴安盟', 'link': 'http://www.iecity.com/xinganmeng/map/Road---b4e5d7af--1.html',
    #   'page': '14'},
    #  {'provincial_capital': '呼伦贝尔', 'link': 'http://www.iecity.com/hulunbeier/map/Road---b4e5d7af--1.html',
    #   'page': '14'},
    #  {'provincial_capital': '赤峰', 'link': 'http://www.iecity.com/chifeng/map/Road---b4e5d7af--1.html', 'page': '32'},
    #  {'provincial_capital': '通辽', 'link': 'http://www.iecity.com/tongliao/map/Road---b4e5d7af--1.html', 'page': '24'},
    #  {'provincial_capital': '鄂尔多斯', 'link': 'http://www.iecity.com/eerduosi/map/Road---b4e5d7af--1.html', 'page': '33'},
    #  {'provincial_capital': '阿拉善盟', 'link': 'http://www.iecity.com/alashan/map/Road---b4e5d7af--1.html', 'page': '14'},
    #  {'provincial_capital': '巴彦淖尔盟', 'link': 'http://www.iecity.com/bayannaoer/map/Road---b4e5d7af--1.html',
    #   'page': '11'},
    #  {'provincial_capital': '锡林郭勒盟', 'link': 'http://www.iecity.com/xilinguole/map/Road---b4e5d7af--1.html',
    #   'page': '15'},
    #  {'provincial_capital': '银川', 'link': 'http://www.iecity.com/yinchuan/map/Road---b4e5d7af--1.html', 'page': '12'},
    #  {'provincial_capital': '中卫', 'link': 'http://www.iecity.com/zhongwei/map/Road---b4e5d7af--1.html', 'page': '11'},
    #  {'provincial_capital': '吴忠', 'link': 'http://www.iecity.com/wuzhong/map/Road---b4e5d7af--1.html', 'page': '14'},
    #  {'provincial_capital': '石嘴山', 'link': 'http://www.iecity.com/shizuishan/map/Road---b4e5d7af--1.html',
    #   'page': '12'},
    #  {'provincial_capital': '固原', 'link': 'http://www.iecity.com/guyuan/map/Road---b4e5d7af--1.html', 'page': '18'},
    #  {'provincial_capital': '西宁', 'link': 'http://www.iecity.com/xining/map/Road---b4e5d7af--1.html', 'page': '11'},
    #  {'provincial_capital': '海东地区', 'link': 'http://www.iecity.com/haidong/map/Road---b4e5d7af--1.html', 'page': '5'},
    #  {'provincial_capital': '海北州', 'link': 'http://www.iecity.com/haibei/map/Road---b4e5d7af--1.html', 'page': '10'},
    #  {'provincial_capital': '海南州', 'link': 'http://www.iecity.com/hainan/map/Road---b4e5d7af--1.html', 'page': '11'},
    #  {'provincial_capital': '果洛州', 'link': 'http://www.iecity.com/guoluo/map/Road---b4e5d7af--1.html', 'page': '7'},
    #  {'provincial_capital': '黄南州', 'link': 'http://www.iecity.com/huangnan/map/Road---b4e5d7af--1.html', 'page': '7'},
    #  {'provincial_capital': '玉树州', 'link': 'http://www.iecity.com/yushu/map/Road---b4e5d7af--1.html', 'page': '9'},
    #  {'provincial_capital': '海西州', 'link': 'http://www.iecity.com/haixi/map/Road---b4e5d7af--1.html', 'page': '8'},
    #  {'provincial_capital': '太原', 'link': 'http://www.iecity.com/taiyuan/map/Road---b4e5d7af--1.html', 'page': '19'},
    #  {'provincial_capital': '临汾', 'link': 'http://www.iecity.com/linfen/map/Road---b4e5d7af--1.html', 'page': '32'},
    #  {'provincial_capital': '吕梁', 'link': 'http://www.iecity.com/lvliang/map/Road---b4e5d7af--1.html', 'page': '33'},
    #  {'provincial_capital': '大同', 'link': 'http://www.iecity.com/datong/map/Road---b4e5d7af--1.html', 'page': '15'},
    #  {'provincial_capital': '忻州', 'link': 'http://www.iecity.com/xinzhou/map/Road---b4e5d7af--1.html', 'page': '22'},
    #  {'provincial_capital': '晋中', 'link': 'http://www.iecity.com/jinzhong/map/Road---b4e5d7af--1.html', 'page': '30'},
    #  {'provincial_capital': '晋城', 'link': 'http://www.iecity.com/jincheng/map/Road---b4e5d7af--1.html', 'page': '31'},
    #  {'provincial_capital': '朔州', 'link': 'http://www.iecity.com/shuozhou/map/Road---b4e5d7af--1.html', 'page': '12'},
    #  {'provincial_capital': '运城', 'link': 'http://www.iecity.com/yuncheng/map/Road---b4e5d7af--1.html', 'page': '30'},
    #  {'provincial_capital': '长治', 'link': 'http://www.iecity.com/changzhi/map/Road---b4e5d7af--1.html', 'page': '41'},
    #  {'provincial_capital': '阳泉', 'link': 'http://www.iecity.com/yangquan/map/Road---b4e5d7af--1.html', 'page': '13'},
    #  {'provincial_capital': '济南', 'link': 'http://www.iecity.com/jinan/map/Road---b4e5d7af--1.html', 'page': '57'},
    #  {'provincial_capital': '青岛', 'link': 'http://www.iecity.com/qingdao/map/Road---b4e5d7af--1.html', 'page': '37'},
    #  {'provincial_capital': '淄博', 'link': 'http://www.iecity.com/zibo/map/Road---b4e5d7af--1.html', 'page': '22'},
    #  {'provincial_capital': '德州', 'link': 'http://www.iecity.com/dezhou/map/Road---b4e5d7af--1.html', 'page': '33'},
    #  {'provincial_capital': '烟台', 'link': 'http://www.iecity.com/yantai/map/Road---b4e5d7af--1.html', 'page': '30'},
    #  {'provincial_capital': '潍坊', 'link': 'http://www.iecity.com/weifang/map/Road---b4e5d7af--1.html', 'page': '42'},
    #  {'provincial_capital': '泰安', 'link': 'http://www.iecity.com/taian/map/Road---b4e5d7af--1.html', 'page': '32'},
    #  {'provincial_capital': '东营', 'link': 'http://www.iecity.com/dongying/map/Road---b4e5d7af--1.html', 'page': '19'},
    #  {'provincial_capital': '威海', 'link': 'http://www.iecity.com/weihai/map/Road---b4e5d7af--1.html', 'page': '16'},
    #  {'provincial_capital': '临沂', 'link': 'http://www.iecity.com/linyi/map/Road---b4e5d7af--1.html', 'page': '42'},
    #  {'provincial_capital': '日照', 'link': 'http://www.iecity.com/rizhao/map/Road---b4e5d7af--1.html', 'page': '22'},
    #  {'provincial_capital': '枣庄', 'link': 'http://www.iecity.com/zaozhuang/map/Road---b4e5d7af--1.html', 'page': '21'},
    #  {'provincial_capital': '济宁', 'link': 'http://www.iecity.com/jining/map/Road---b4e5d7af--1.html', 'page': '34'},
    #  {'provincial_capital': '滨州', 'link': 'http://www.iecity.com/binzhou/map/Road---b4e5d7af--1.html', 'page': '31'},
    #  {'provincial_capital': '聊城', 'link': 'http://www.iecity.com/liaocheng/map/Road---b4e5d7af--1.html', 'page': '34'},
    #  {'provincial_capital': '莱芜', 'link': 'http://www.iecity.com/laiwu/map/Road---b4e5d7af--1.html', 'page': '0'},
    #  {'provincial_capital': '菏泽', 'link': 'http://www.iecity.com/heze/map/Road---b4e5d7af--1.html', 'page': '42'},
    #  {'provincial_capital': '西安', 'link': 'http://www.iecity.com/xian/map/Road---b4e5d7af--1.html', 'page': '51'},
    #  {'provincial_capital': '咸阳', 'link': 'http://www.iecity.com/xianyang/map/Road---b4e5d7af--1.html', 'page': '24'},
    #  {'provincial_capital': '延安', 'link': 'http://www.iecity.com/yanan/map/Road---b4e5d7af--1.html', 'page': '30'},
    #  {'provincial_capital': '宝鸡', 'link': 'http://www.iecity.com/baoji/map/Road---b4e5d7af--1.html', 'page': '43'},
    #  {'provincial_capital': '商洛', 'link': 'http://www.iecity.com/shangluo/map/Road---b4e5d7af--1.html', 'page': '28'},
    #  {'provincial_capital': '安康', 'link': 'http://www.iecity.com/ankang/map/Road---b4e5d7af--1.html', 'page': '46'},
    #  {'provincial_capital': '榆林', 'link': 'http://www.iecity.com/yuulin/map/Road---b4e5d7af--1.html', 'page': '52'},
    #  {'provincial_capital': '汉中', 'link': 'http://www.iecity.com/hanzhong/map/Road---b4e5d7af--1.html', 'page': '70'},
    #  {'provincial_capital': '渭南', 'link': 'http://www.iecity.com/weinan/map/Road---b4e5d7af--1.html', 'page': '33'},
    #  {'provincial_capital': '铜川', 'link': 'http://www.iecity.com/tongchuan/map/Road---b4e5d7af--1.html', 'page': '16'},
    #  {'provincial_capital': '成都', 'link': 'http://www.iecity.com/chengdu/map/Road---b4e5d7af--1.html', 'page': '79'},
    #  {'provincial_capital': '自贡', 'link': 'http://www.iecity.com/zigong/map/Road---b4e5d7af--1.html', 'page': '21'},
    #  {'provincial_capital': '绵阳', 'link': 'http://www.iecity.com/mianyang/map/Road---b4e5d7af--1.html', 'page': '53'},
    #  {'provincial_capital': '泸州', 'link': 'http://www.iecity.com/luzhou/map/Road---b4e5d7af--1.html', 'page': '56'},
    #  {'provincial_capital': '宜宾', 'link': 'http://www.iecity.com/yibin/map/Road---b4e5d7af--1.html', 'page': '48'},
    #  {'provincial_capital': '内江', 'link': 'http://www.iecity.com/neijiang/map/Road---b4e5d7af--1.html', 'page': '22'},
    #  {'provincial_capital': '资阳', 'link': 'http://www.iecity.com/ziyang/map/Road---b4e5d7af--1.html', 'page': '26'},
    #  {'provincial_capital': '乐山', 'link': 'http://www.iecity.com/leshan/map/Road---b4e5d7af--1.html', 'page': '39'},
    #  {'provincial_capital': '眉山', 'link': 'http://www.iecity.com/meishan/map/Road---b4e5d7af--1.html', 'page': '14'},
    #  {'provincial_capital': '凉山', 'link': 'http://www.iecity.com/liangshan/map/Road---b4e5d7af--1.html', 'page': '47'},
    #  {'provincial_capital': '南充', 'link': 'http://www.iecity.com/nanchong/map/Road---b4e5d7af--1.html', 'page': '40'},
    #  {'provincial_capital': '巴中', 'link': 'http://www.iecity.com/bazhong/map/Road---b4e5d7af--1.html', 'page': '50'},
    #  {'provincial_capital': '广元', 'link': 'http://www.iecity.com/guangyuan/map/Road---b4e5d7af--1.html', 'page': '59'},
    #  {'provincial_capital': '广安', 'link': 'http://www.iecity.com/guangan/map/Road---b4e5d7af--1.html', 'page': '23'},
    #  {'provincial_capital': '德阳', 'link': 'http://www.iecity.com/deyang/map/Road---b4e5d7af--1.html', 'page': '32'},
    #  {'provincial_capital': '攀枝花', 'link': 'http://www.iecity.com/panzhihua/map/Road---b4e5d7af--1.html', 'page': '19'},
    #  {'provincial_capital': '甘孜', 'link': 'http://www.iecity.com/ganzi/map/Road---b4e5d7af--1.html', 'page': '25'},
    #  {'provincial_capital': '达州', 'link': 'http://www.iecity.com/dazhou/map/Road---b4e5d7af--1.html', 'page': '47'},
    #  {'provincial_capital': '遂宁', 'link': 'http://www.iecity.com/suining/map/Road---b4e5d7af--1.html', 'page': '22'},
    #  {'provincial_capital': '阿坝', 'link': 'http://www.iecity.com/aba/map/Road---b4e5d7af--1.html', 'page': '22'},
    #  {'provincial_capital': '雅安', 'link': 'http://www.iecity.com/yaan/map/Road---b4e5d7af--1.html', 'page': '20'},
    #  {'provincial_capital': '乌鲁木齐', 'link': 'http://www.iecity.com/wulumuqi/map/Road---b4e5d7af--1.html', 'page': '13'},
    #  {'provincial_capital': '伊犁州', 'link': 'http://www.iecity.com/yili/map/Road---b4e5d7af--1.html', 'page': '15'},
    #  {'provincial_capital': '克拉玛依', 'link': 'http://www.iecity.com/kelamayi/map/Road---b4e5d7af--1.html', 'page': '1'},
    #  {'provincial_capital': '博尔塔拉', 'link': 'http://www.iecity.com/boertala/map/Road---b4e5d7af--1.html', 'page': '7'},
    #  {'provincial_capital': '吐鲁番', 'link': 'http://www.iecity.com/tulufan/map/Road---b4e5d7af--1.html', 'page': '4'},
    #  {'provincial_capital': '塔城', 'link': 'http://www.iecity.com/tacheng/map/Road---b4e5d7af--1.html', 'page': '15'},
    #  {'provincial_capital': '昌吉', 'link': 'http://www.iecity.com/changji/map/Road---b4e5d7af--1.html', 'page': '13'},
    #  {'provincial_capital': '石河子', 'link': 'http://www.iecity.com/shihezi/map/Road---b4e5d7af--1.html', 'page': '2'},
    #  {'provincial_capital': '阿克苏', 'link': 'http://www.iecity.com/akesu/map/Road---b4e5d7af--1.html', 'page': '21'},
    #  {'provincial_capital': '阿勒泰', 'link': 'http://www.iecity.com/aletai/map/Road---b4e5d7af--1.html', 'page': '18'},
    #  {'provincial_capital': '巴音郭楞', 'link': 'http://www.iecity.com/bayinguoleng/map/Road---b4e5d7af--1.html',
    #   'page': '16'},
    #  {'provincial_capital': '哈密地区', 'link': 'http://www.iecity.com/hami/map/Road---b4e5d7af--1.html', 'page': '9'},
    #  {'provincial_capital': '和田地区', 'link': 'http://www.iecity.com/hetian/map/Road---b4e5d7af--1.html', 'page': '16'},
    #  {'provincial_capital': '喀什地区', 'link': 'http://www.iecity.com/kashi/map/Road---b4e5d7af--1.html', 'page': '31'},
    #  {'provincial_capital': '克孜勒苏', 'link': 'http://www.iecity.com/kezilesu/map/Road---b4e5d7af--1.html', 'page': '13'},
    #  {'provincial_capital': '北屯', 'link': 'http://www.iecity.com/beitun/map/Road---b4e5d7af--1.html', 'page': '0'},
    #  {'provincial_capital': '铁门关', 'link': 'http://www.iecity.com/tiemenguan/map/Road---b4e5d7af--1.html', 'page': '0'},
    #  {'provincial_capital': '双河', 'link': 'http://www.iecity.com/shuanghe/map/Road---b4e5d7af--1.html', 'page': '1'},
    #  {'provincial_capital': '可克达拉', 'link': 'http://www.iecity.com/kekedala/map/Road---b4e5d7af--1.html', 'page': '1'},
    #  {'provincial_capital': '昆玉', 'link': 'http://www.iecity.com/kunyu/map/Road---b4e5d7af--1.html', 'page': '1'},
    #  {'provincial_capital': '五家渠', 'link': 'http://www.iecity.com/wujiaju/map/Road---b4e5d7af--1.html', 'page': '1'},
    #  {'provincial_capital': '阿拉尔', 'link': 'http://www.iecity.com/alaer/map/Road---b4e5d7af--1.html', 'page': '0'},
    #  {'provincial_capital': '图木舒克', 'link': 'http://www.iecity.com/tumushuke/map/Road---b4e5d7af--1.html', 'page': '0'},
    #  {'provincial_capital': '香港', 'link': 'http://www.iecity.com/xianggang/map/Road---b4e5d7af--1.html', 'page': '16'},
    #  {'provincial_capital': '拉萨', 'link': 'http://www.iecity.com/lasa/map/Road---b4e5d7af--1.html', 'page': '16'},
    #  {'provincial_capital': '山南地区', 'link': 'http://www.iecity.com/shannan/map/Road---b4e5d7af--1.html', 'page': '14'},
    #  {'provincial_capital': '日喀则', 'link': 'http://www.iecity.com/rikaze/map/Road---b4e5d7af--1.html', 'page': '21'},
    #  {'provincial_capital': '阿里地区', 'link': 'http://www.iecity.com/ali/map/Road---b4e5d7af--1.html', 'page': '10'},
    #  {'provincial_capital': '昌都地区', 'link': 'http://www.iecity.com/changdu/map/Road---b4e5d7af--1.html', 'page': '20'},
    #  {'provincial_capital': '林芝地区', 'link': 'http://www.iecity.com/linzhi/map/Road---b4e5d7af--1.html', 'page': '12'},
    #  {'provincial_capital': '那曲地区', 'link': 'http://www.iecity.com/naqu/map/Road---b4e5d7af--1.html', 'page': '14'},
    #  {'provincial_capital': '昆明', 'link': 'http://www.iecity.com/kunming/map/Road---b4e5d7af--1.html', 'page': '39'},
    #  {'provincial_capital': '玉溪', 'link': 'http://www.iecity.com/yuxi/map/Road---b4e5d7af--1.html', 'page': '21'},
    #  {'provincial_capital': '大理', 'link': 'http://www.iecity.com/dali/map/Road---b4e5d7af--1.html', 'page': '34'},
    #  {'provincial_capital': '昭通', 'link': 'http://www.iecity.com/zhaotong/map/Road---b4e5d7af--1.html', 'page': '37'},
    #  {'provincial_capital': '曲靖', 'link': 'http://www.iecity.com/qujing/map/Road---b4e5d7af--1.html', 'page': '43'},
    #  {'provincial_capital': '楚雄', 'link': 'http://www.iecity.com/chuxiong/map/Road---b4e5d7af--1.html', 'page': '33'},
    #  {'provincial_capital': '红河', 'link': 'http://www.iecity.com/honghe/map/Road---b4e5d7af--1.html', 'page': '27'},
    #  {'provincial_capital': '西双版纳', 'link': 'http://www.iecity.com/xishuangbanna/map/Road---b4e5d7af--1.html',
    #   'page': '12'},
    #  {'provincial_capital': '保山', 'link': 'http://www.iecity.com/baoshan/map/Road---b4e5d7af--1.html', 'page': '25'},
    #  {'provincial_capital': '德宏州', 'link': 'http://www.iecity.com/dehong/map/Road---b4e5d7af--1.html', 'page': '15'},
    #  {'provincial_capital': '迪庆州', 'link': 'http://www.iecity.com/diqing/map/Road---b4e5d7af--1.html', 'page': '11'},
    #  {'provincial_capital': '丽江', 'link': 'http://www.iecity.com/lijiang/map/Road---b4e5d7af--1.html', 'page': '17'},
    #  {'provincial_capital': '临沧地区', 'link': 'http://www.iecity.com/lincang/map/Road---b4e5d7af--1.html', 'page': '12'},
    #  {'provincial_capital': '怒江州', 'link': 'http://www.iecity.com/nujiang/map/Road---b4e5d7af--1.html', 'page': '13'},
    #  {'provincial_capital': '普洱', 'link': 'http://www.iecity.com/puer/map/Road---b4e5d7af--1.html', 'page': '27'},
    #  {'provincial_capital': '文山州', 'link': 'http://www.iecity.com/wenshan/map/Road---b4e5d7af--1.html', 'page': '31'},
    #  {'provincial_capital': '杭州', 'link': 'http://www.iecity.com/hangzhou/map/Road---b4e5d7af--1.html', 'page': '74'},
    #  {'provincial_capital': '嘉兴', 'link': 'http://www.iecity.com/jiaxing/map/Road---b4e5d7af--1.html', 'page': '77'},
    #  {'provincial_capital': '绍兴', 'link': 'http://www.iecity.com/shaoxing/map/Road---b4e5d7af--1.html', 'page': '37'},
    #  {'provincial_capital': '湖州', 'link': 'http://www.iecity.com/huzhou/map/Road---b4e5d7af--1.html', 'page': '32'},
    #  {'provincial_capital': '宁波', 'link': 'http://www.iecity.com/ningbo/map/Road---b4e5d7af--1.html', 'page': '69'},
    #  {'provincial_capital': '台州', 'link': 'http://www.iecity.com/taiizhou/map/Road---b4e5d7af--1.html', 'page': '31'},
    #  {'provincial_capital': '温州', 'link': 'http://www.iecity.com/wenzhou/map/Road---b4e5d7af--1.html', 'page': '44'},
    #  {'provincial_capital': '金华', 'link': 'http://www.iecity.com/jinhua/map/Road---b4e5d7af--1.html', 'page': '37'},
    #  {'provincial_capital': '舟山', 'link': 'http://www.iecity.com/zhoushan/map/Road---b4e5d7af--1.html', 'page': '30'},
    #  {'provincial_capital': '丽水', 'link': 'http://www.iecity.com/lishui/map/Road---b4e5d7af--1.html', 'page': '37'},
    #  {'provincial_capital': '衢州', 'link': 'http://www.iecity.com/quzhou/map/Road---b4e5d7af--1.html', 'page': '36'}]

    # item['provincial_capital'] = city



get_city()