
# -*- coding: utf-8 -*-
# @Time    : 2019/7/15 9:58
# @Author  : admin
# @Software: PyCharm
import datetime
import re
import time
import requests
from urllib.parse import urljoin, urlparse
import base64
import hashlib
from zhaobiao.tools.filter_time import Times
from lxml import html as ltml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Utils_(object):
    t = Times()

    # md5 hash值 即所需的id值
    def url_hash(self, url):
        md = hashlib.md5()
        md.update(url.replace("http://", "").replace("https://", "").encode('utf-8'))
        m = md.digest()
        hash = str(base64.b64encode(m), encoding='utf-8').replace("/", "").replace("+", "").replace("=", "")
        return hash

    # 浏览器获取源码
    def login(ip):
        chrome_options = Options()
        # 设置无头界面
        chrome_options.add_argument('--headless')
        # 禁止加载图片\js
        # prefs={
        #      'profile.default_content_setting_values': {
        #         'images': 2,
        #         'javascript': 2
        #     }
        # }
        #     prefs={
        #          'profile.default_content_setting_values': {
        #             'images': 2,
        #         }
        #     }
        # chrome_options.add_experimental_option('prefs',prefs)
        # 设置跨域访问
        chrome_options.add_argument("--args --disable-web-security")
        # 搜狗浏览器请求头
        chrome_options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36 SE 2.X MetaSr 1.0"')
        # 开发者模式，防止检测到slenium
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

        chrome_options.add_experimental_option('useAutomationExtension', False)
        # 禁用启用Blink运行时的功能
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # 隐身模式
        # chrome_options.add_argument('--incognito')
        # 不打印日志信息
        chrome_options.add_argument('log-level=3')

        path = r'D:\TX-project\requests\zhaobiao\zhaobiao\tools\chromedriver.exe'
        # path = os.getcwd()+'\chromedriver.exe'
        if ip == '':
            browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
        else:
            PROXY = "http://{}".format(ip)
            options = webdriver.ChromeOptions()
            desired_capabilities = options.to_capabilities()
            desired_capabilities['proxy'] = {
                "httpProxy": PROXY,
                "ftpProxy": PROXY,
                "sslProxy": PROXY,
                "noProxy": None,
                "proxyType": "MANUAL",
                "class": "org.openqa.selenium.Proxy",
                "autodetect": False
            }
            browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options,
                                       desired_capabilities=desired_capabilities)
        # 设置webdriver.navigator
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""}
                                )
        browser.execute_script("Object.defineProperties(navigator,{ webdriver:{ get: () => false } })");
        browser.implicitly_wait(10)
        # browser.set_window_size(600,800)

        return browser

    # 提取时间 借鉴github
    def extract_pubtime(self, div_text):
        pubtime = ''
        pubtime = re.search(
            r'(\d{4}\s*[年\-:/]\s*)\d{1,2}\s*[月\-：/]\s*\d{1,2}\s*[\-_:日]?\s*\d{1,2}\s*:\s*\d{1,2}\s*(:\s*\d{1,2})?',
            div_text, flags=re.S | re.I)
        if pubtime:
            pubtime = pubtime.group()
        if not pubtime:
            pubtime = re.search(r'(\d{4}\s*[年\-:/]\s*)\d{1,2}\s*[月\-：/]\s*\d{1,2}\s*[\-_:日/]?', div_text,
                                flags=re.S)
            if pubtime:
                pubtime = pubtime.group()
        if pubtime:
            pubtime = pubtime.strip()
            pubtime = pubtime.replace('年', '-').replace('月', '-').replace('日', ' ').replace('/', '-')
            pubtime = self.drop_mutil_blank(pubtime)
            return pubtime
        else:
            return pubtime

    def drop_mutil_blank(self, str):
        str = re.sub(r'\s{2,}', ' ', str)
        return str



    # 提取作者信息
    def extract_author(self, text):
        # pattern = re.compile('[\s\S]+[编辑|记者|责编|作者|来源][:|：].*?([\S\s][\u4E00-\u9FA5]+)', re.S)
        pattern = re.compile('[\s\S]+[作者|编辑|记者|责编|来源][:|：].*?([\S\s][\u4E00-\u9FA5]+)', re.S)
        # match_re = re.search(pattern, text)
        match_re = re.search(pattern, text)
        return match_re.group(1)

    def find_all_urls_old(self, url, html):
        from scrapy.selector import Selector
        if not html is None:
            response = Selector(text=html)
            result = urlparse(url)
            domain_ = result.netloc
            urls_list = response.css("::attr(href)").extract()
            if urls_list:
                filter_urls = [urls.replace(' ', '') for urls in urls_list]
                filter_urls = [urljoin(url, urls) for urls in filter_urls]
                filter_urls = [url for url in filter_urls if
                               '.css' not in url and 'javascript:' not in url and '.js' not in url \
                               and '.ico' not in url and '{%' not in url and '.xml' not in url and len(url) > 7]
                domain_urls = [i for i in filter_urls if domain_ in i]
                filter_url = [i for i in domain_urls if not i.endswith('/') if not i.endswith('+')]
                filter_url_list = ['/' + str(i) + '/' for i in range(2008, 2019)]
                filter_url_list += ['.jpg', '.png', 'list-', 'username', '-uid-',
                                    'uid=', '_list_', '.pdf', '.xml']

                def filter_(filter_url, filter_url_list):
                    new_urls = []
                    for i in filter_url:
                        for j in filter_url_list:
                            if j in i:
                                continue
                            new_urls.append(i)
                    return new_urls

                find_all_url = filter_(filter_url, filter_url_list)
                return set(find_all_url)
            else:
                return None

    def find_all_urls(self, url, html):
        from scrapy.selector import Selector
        if not html is None:
            response = Selector(text=html)
            result = urlparse(url)
            domain_ = result.netloc
            urls_list_all = response.css("a:link")
            urls_list_1 = [url.css('::attr(href)').extract_first() for url in urls_list_all]
            urls_list_2 = [url.css('::text').extract_first() for url in urls_list_all]

            # 先过滤一遍url标题小于5个的
            def filter_old(urls_list_1, urls_list_2):
                urls = []
                for url, text in zip(urls_list_1, urls_list_2):
                    if text == '' or text is None or len(str(text)) < 5:
                        continue
                    # print('url',url)
                    # print('text',text)
                    urls.append(url)
                return urls

            urls_list = filter_old(urls_list_1, urls_list_2)
            if urls_list:
                filter_urls = [urls.replace(' ', '') for urls in urls_list]
                filter_urls = [urljoin(url, urls) for urls in filter_urls]
                filter_urls = [url for url in filter_urls if
                               '.css' not in url and 'javascript:' not in url and '.js' not in url \
                               and '.ico' not in url and '{%' not in url and '.xml' not in url and len(url) > 7]
                domain_urls = [i for i in filter_urls if domain_ in i]
                filter_urls = [i for i in domain_urls if not i.endswith('/') if not i.endswith('+')]
                filter_url_list = ['/' + str(i) + '/' for i in range(2008, 2019)]
                filter_url_list += ['.jpg', '.png', 'list-', 'username', '-uid-',
                                    'uid=', '_list_', '.pdf', '.xml']

                # 过滤大部分杂乱的链接
                def filter_(filter_url, filter_url_list):
                    new_urls = []
                    for i in filter_url:
                        for j in filter_url_list:
                            if j in i:
                                continue
                            new_urls.append(i)
                    return new_urls

                find_all_url = filter_(filter_urls, filter_url_list)
                # 返回 去重后的Url
                return set(find_all_url)
            else:
                return None

    @classmethod
    def remove_html_tags(cls, html):
        html = html.replace('&lt;', '<').replace('&gt;', '>')
        element = ltml.fromstring(html)
        text = ltml.tostring(element, encoding='unicode')
        strTemp = re.sub("<[\\s]*?script[^>]*?>[\\s\\S]*?<[\\s]*?\\/[\\s]*?script[\\s]*?>", "", text)
        str2Temp = re.sub("<[\\s]*?style[^>]*?>[\\s\\S]*?<[\\s]*?\\/[\\s]*?style[\\s]*?>", "", strTemp)
        str3Temp = re.sub("<[^>]+>", "", str2Temp)
        content = ' '.join(str3Temp.replace('&gt;', '').replace('&nbsp;', '').strip().split())
        return content

    @classmethod
    def re_pubdate(cls,tag_str):
        res = re.findall('\s*(\d{4})[-/.+](\d{1,2})[-/.+](\d{1,2})[\s*|\w{1,4}]\s*(\d{1,2}:\d{1,2}:\d{1,2})', tag_str)
        data = ' '.join(list(res[0]))
        return data

    @classmethod
    def md5_encrypt(cls, chart):
        md = hashlib.md5(chart.encode())
        return md.hexdigest()

    @classmethod
    def re_muber(cls,string):
        try:
            result = int(re.search('(\d+)',string).group(1))
        except:
            result = 0
        return result

if __name__ == '__main__':

    u = Utils_()
    a = '''<time datetime="2020-04-24T15:17:14" data-format="article-display" data-show-date="always" data-show-time="today-only" data-timestamp="1587737834" itemprop="datePublished" class="article-timestamp formatTimeStampEs6" full-date="24.04.2020">\xa0\n            </time>'''
    start_time = time.time()
    print(u.remove_html_tags(a))
    print('Time', time.time() - start_time)
    a = u.re_pubdate("""<time class="article-timestamp" datetime="2020-04-27T15:43:03.667-04:00" itemprop="datePublished" data-editable="publishedDate">
              <span class="article-date">3:43 P.M.</span>
          </time> """)
    print(a)