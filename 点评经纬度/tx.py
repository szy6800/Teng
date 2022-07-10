import requests
from lxml import etree
from selenium import webdriver
# from fake_useragent import UserAgent

class tencent_movie(object):
    def __init__(self):

        # ua = UserAgent(verify_ssl=False)
        for i in range(1, 100):
            self.headers = {
                # 'User-Agent': ua.random
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
                }
    def get_html(self,url):
        response=requests.get(url,headers=self.headers)
        html=response.content.decode('utf-8')
        return html

    def parse_html_tengxun(self,html):
        target=etree.HTML(html)
        links = target.xpath('//h2[@class="result_title"]/a/@href')
        host=links[0]
        res = requests.get(host, headers=self.headers)
        con = res.content.decode('utf-8')
        new_html = etree.HTML(con)
        first_select = int(input('1.电视剧\n2.电影\n'))
        if (first_select == 1):
            titles=new_html.xpath('//div[@class="mod_episode"]/span/a/span/text()')
            new_links=new_html.xpath('//div[@class="mod_episode"]/span/a/@href')
            for title in titles:
                print('第%s集'%title)
            select = int(input('你要看第几集：(输入数字即可)'))
            new_link = new_links[select - 1]
            last_host = 'https://api.akmov.net/?url=' + new_link
        else:
            last_host = 'https://api.akmov.net/?url=' + host
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(last_host)
    def main(self):
        name = str(input('请输入电视剧或电影名：'))
        url = 'https://v.qq.com/x/search/?q={}&stag=0&smartbox_ab='.format(name)
        html = self.get_html(url)
        self.parse_html_tengxun(html)

if __name__ == '__main__':
    spider=tencent_movie()
    spider.main()