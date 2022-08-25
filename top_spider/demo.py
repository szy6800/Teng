import requests
import jsonpath
from lxml import etree
import csv
import time

# 商户信息
def meituan():
    for i in range(0,32,32):
        url = f'https://apimobile.meituan.com/group/v4/poi/pcsearch/60?uuid=6d55751f050e4ee59b93.1652929619.1.0.0&userid=10941461&limit=32&offset={i}&cateId=195&q=%E9%BB%84%E5%B2%9B%E5%8C%BA&token=PS6PtjqCXdTuv6njP_LC2zNImmcFAAAA-REAAJlUNXhbu7vfrQjVwjgU7_Ac9t2ey10mz2H3gJ9O6Z6PayMdaso-0ugQREq9hoRQ1Q&areaId=-1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        }
        response = requests.get(url, headers=headers,).json()
        datas = jsonpath.jsonpath(response,'$..searchResult')
        for data in datas[0]:
            # 解析商品页
            id = data['id']
            photo = data['imageUrl']
            name = data['title']
            score = data['avgscore']
            consumption_per_person = data['avgprice']
            label = data['backCateName']
            label1 = data['areaname']
            Comment_on_the_amount = data['comments']
            set_meals = jsonpath.jsonpath(data['abstracts'], '$..message')
            set_meal = ''
            if type(set_meals) == list:
                set_meal += set_meals[0]
            else:
                pass
            cont = [name,id,photo,score,consumption_per_person,label,label1,Comment_on_the_amount,set_meal]
            particulars(id,cont,Comment_on_the_amount)


# 商品详情页
def particulars(id,cont,Comment_on_the_amount):
    url = f'https://www.meituan.com/zhoubianyou/{id}/'
    headers = {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    moudle = etree.HTML(response.text)
    site = moudle.xpath('//*[@id="react"]/div/div/div[2]/div[1]/div[2]/div[1]/a/span//text()')
    y_times= moudle.xpath('//*[@id="react"]/div/div/div[2]/div[1]/div[2]/div[2]/span[2]/text()')
    phones = moudle.xpath('//*[@id="lego-widget-play-mt-poi-001-000"]/div/div[2]/div[1]/div[2]/div[2]/span[2]//text()')
    # 判断是否为黄岛区
    sf = 0
    if '黄岛区' in site[0]:
        sf+=1
    else:
        pass
    y_time = ''
    for ti in y_times:
        y_time+=ti
    phone = ''
    for ph in phones:
        phone+=ph
    cont.append(site[0])
    cont.append(sf)
    cont.append(y_time)
    cont.append(phone)
    meituan_comment(id,Comment_on_the_amount,cont)


# 评论
def meituan_comment(id,Comment_on_the_amount,cont):
    for i in range(0,Comment_on_the_amount,10):
        url = f'https://www.meituan.com/ptapi/poi/getcomment?id={id}&offset={i}&pageSize=10&mode=0&starRange=&userId=&sortType=0'
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        }
        response = requests.get(url, headers=headers,allow_redirects=False).json()
        datas = jsonpath.jsonpath(response,'$..comments')
        for data in datas[0]:
            # print(data)
            # 解析评论
            username = data['userName']
            user_photo = data['userUrl']
            text = data['comment']

            # 格式时间
            pl_times = data['commentTime']
            timeTemp = float(int(pl_times) / 1000)
            tupTime = time.localtime(timeTemp)
            pl_time = time.strftime("%Y-%m-%d %H:%M:%S", tupTime)

            pl_photos = jsonpath.jsonpath(data['picUrls'],'$..url')
            xiaofei = data['menu']

            pl_photo = ''
            if type(pl_photos) == list:
                for li in pl_photos:
                    pl_photo = pl_photo+' '+li
            else:
                pass
            add = [username,user_photo,xiaofei,text,pl_time,pl_photo]
            coon = cont+add
            print(coon)
            storage1(coon)

# 数据表字段
def storage0():
    with open('meituan1.csv','a',newline='',encoding='utf-8-sig') as f:
        q = csv.writer(f,dialect='excel')
        q.writerow(['商家','商家id','商家logo','店铺评分','人均消费','标签','子标签','评论量','套餐','地址','是否在黄岛区(1/0)','营业时间','电话','评价用户名','用户头像','具体消费','评价内容','发布时间','评论图片'])

# 数据表字段
def storage1(coon):
    with open('meituan1.csv','a',newline='',encoding='utf-8-sig') as f:
        q = csv.writer(f,dialect='excel')
        q.writerow(coon)

# 运行
def run():
    storage0()
    meituan()


if __name__ == '__main__':
    run()
