#-*-coding:utf-8-*-
import hashlib
import requests
import re
import time
import json
from sqlalchemy import create_engine
from collections import defaultdict, OrderedDict
import pandas as pd




def countent():
    with open('中国市场.txt', 'rb') as f:
        countent = f.read().decode()
        countent = countent.replace('null','"null"').replace('true','"true"')
        # countent = re.search('"searchResultRecord":(.*?),"ssId"', countent).group(1)
    f.close()
    return json.loads(countent)


def items():
    item = OrderedDict()
    # item['id'] = ''
    item['uid'] = '' # 去重
    item['url'] = '' # 链接
    item['PRJNUM'] = '' # 项目编号
    item['PRJNAME'] = '' # 项目名称
    item['PROVINCEPRJNUM'] = '' # 省级项目编号
    item['BUILDCORPNAME'] = '' # 建设单位
    item['BUILDCORPCODE'] = '' # 建设单位统一社会信用代码
    item['PRJTYPENUM'] = '' # 项目分类
    item['PRJPROPERTYNUM'] = '' # 建设性质
    item['ALLINVEST'] = '' # 总面积（平方米）
    item['ALLAREA'] = '' # 总投资（万元）
    item['PRJAPPROVALLEVELNUM'] = '' # 立项级别
    item['PRJAPPROVALNUM'] = '' # 立项文号
    item['PRJCODE'] = '' # 项目代码
    item['PROVINCE'] = '' # 省
    item['CITY'] = '' # 市
    item['COUNTY'] = '' # 区县
    item['ADDRESS'] = '' # 具体地点
    item['LOCATIONX'] = '' # 经度
    item['LOCATIONY'] = '' # 纬度
    item['PRJAPPROVALDEPART'] = '' # 立项批复机关
    item['PRJAPPROVALDATE'] = '' # 立项批复时间
    item['BUILDPLANNUM'] = '' # 建设用地规划许可证编号
    item['PROJECTPLANNUM'] = '' # 建设工程规划许可证编号
    item['INVPROPERTY'] = '' # 工程投资性质
    item['ALLLENGTH'] = '' # 总长度（米）
    item['PRJFUNCTIONNUM'] = '' # 工程用途
    item['BEGINDATE'] = '' # 计划开工
    item['ENDDATE'] = '' # 计划竣工
    item['DATASOURCENAME'] = '' # 数据来源
    item['DATALEVEL'] = '' # 数据等级



    return item


def md5_encrypt(chart):
    md = hashlib.md5(chart.encode())
    return md.hexdigest()

def item_list(item):
    values = list(item.values())
    return values


def reader(query, db='test'):
    sql = query
    count = 0
    df = ''
    while 1:
        count = count + 1
        try:
            engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/{}?charset=utf8'.format(db))
            df = pd.read_sql(sql, engine)
            engine.dispose()
            break
        except Exception as e:
            print(e)
            time.sleep(1)
            if count > 2:
                input01 = input('无法连接数据库，回车继续！')
                break
            else:
                continue
    return df


def compare_data(df_1, table, db):
    select_sql2 = "select uid from %s" % (table)
    try:
        df_2 = reader(select_sql2, db=db)
    except Exception as e:
        print('目标表不存在:', e)
        return df_1

    if len(df_2) > 0:
        df_2.drop_duplicates(subset='uid', keep='first', inplace=True)
        df_2.rename(columns={'uid': 'idpp'}, inplace=True)

        df_1 = df_1.merge(df_2, how='left', left_on='uid', right_on="idpp")
        df_1['idpp'].fillna(value='', inplace=True)
        print('一共%d条' % len(df_1), end=',')
        df_1 = df_1[df_1['idpp'] == '']
        df_1.drop(columns=['idpp'], inplace=True)
        print('对比后保留%d条' % len(df_1), end=',')
    return df_1


def df_to_mysql(df_all, table2, db):
    df_save = df_all
    if len(df_save) >= 0:
        try:
            engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/{}?charset=utf8'.format(db))
            df_save.to_sql(name=table2,
                           con=engine,
                           if_exists='append', index=False,
                           chunksize=10000)
            print('保存了%d条数据！' % len(df_save))
            engine.dispose()
        except Exception as e:
            df_save.to_csv('./tomysql_error2.csv', index=False)
            print(e)
            input01 = input('写入数据库错误')

            # 抓取之前对比数据库

if __name__ == '__main__':
    # ppp = mabiao()
    # print(ppp)
    # print(type(ppp))

    item = items()
    print(item)


    # browser = login(ip='')
    # browser.get("http://vip.qianlima.com/login.html")
    # time.sleep(10)
    # buttons = browser.find_elements_by_id('usernameInput')
    # buttons[0].click()
    # buttons[0].clear()
    # buttons[0].send_keys('19520198824')
    # time.sleep(1)
    # buttons = browser.find_elements_by_id('passwordInput')
    # buttons[0].click()
    # buttons[0].clear()
    # buttons[0].send_keys('bj001958')
    # time.sleep(1)
    # buttons = browser.find_elements_by_id('deng')
    # buttons[0].click()
    # time.sleep(3)
    # browser.get("http://search.vip.qianlima.com/rest/service/website/search/solr/homePage?numPerPage=10&currentPage=1&isfirst=true&filtermode=1&timeType=101&newAreas=&latestTenderType=1&_=1642413437751")
    # time.sleep(3)
    # clist = browser.get_cookies()
    # print(clist)
    # clist = [x['value'] for x in clist if ('name' in x.keys() and x['name'] == '__jsl_clearance')]
    # print("get_JSESSIONID", clist[0])
    #
    # browser.quit()
    #
    # print(clist[0])






    # url = 'http://zxhy.qianlima.com/rest/mp/search/tenderSearch'
    # url = 'http://search.vip.qianlima.com/rest/service/website/search/solr/homePage?numPerPage=10&currentPage=1&isfirst=true&filtermode=1&timeType=101&newAreas=&latestTenderType=1&_=1642413437751'
    #
    # headers = {
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    #     "Accept-Encoding": "gzip, deflate",
    #     "Accept-Language": "zh-CN,zh;q=0.9",
    #     "Cache-Control": "max-age=0",
    #     "Connection": "keep-alive",
    #     "Cookie": "qlm_rem_login=1; qlm_username=19520198824; qlm_password=UBpBggKB3foEggRmCjEUfEBBgC3pUpUK; 19520198824UBpBggKB3foEggRmCjEUfEBBgC3pUpUK=714f5373-4642-414c-a765-d8bb881feff0; source=1; useragent_hash=a2fdad25d911a8a4b39828759d282361; login_time=1642413493; xAuthToken=6b6abbc6-7b9a-410a-b4fd-476da7c28275; login_ip=123.126.87.122; userInfo={%22userId%229884981%2C%22username%22%2219520198824%22%2C%22userIcon%22%22%22%2C%22linkName%22%22%E8%8B%8F%22%2C%22companyName%22%22%E8%85%BE%E4%BF%A1%22%2C%22areaId%22%222703%22%2C%22areaName%22%22%E5%85%A8%E5%9B%BD%22%2C%22roleId%221%2C%22roleName%22%22%E7%AE%A1%E7%90%86%E5%91%98%22%2C%22sex%22%22m%22%2C%22expireDate%22%222024-09-05%22%2C%22isExpired%220%2C%22maxChildCount%220%2C%22isUsedCount%220%2C%22userStatus%221%2C%22memberLevel%2220%2C%22memberLevelName%22%22%E6%99%AE%E9%80%9A%E4%BC%9A%E5%91%98%22%2C%22registerTime%22%222021-12-24%22%2C%22isSuperSupplier%220%2C%22isNewUser%221%2C%22welcomeMsg%22%22%E6%AC%A2%E8%BF%8E%E8%BF%9B%E5%85%A5%E5%8D%83%E9%87%8C%E9%A9%AC%E6%8B%9B%E6%A0%87%E7%BD%91%EF%BD%9E%22%2C%22customerServiceInfo%22{%22id%2262%2C%22customerServiceName%22%22%E8%B4%BA%E4%B8%B9%22%2C%22weChatIcon%22%22http://img_al.qianlima.com/invoice/1621998294_e6affd51e6.png%22%2C%22customerServicePhone%22%22400-900-6616%22%2C%22customerServiceQQ%22%22%22%2C%22customerServiceEmail%22%22kefu@qianlima.com%22}%2C%22shouji%22%2218601157993%22%2C%22email%22%22%22%2C%22dwmc%22%22%E8%85%BE%E4%BF%A1%22%2C%22zhiwu%22%22%E5%95%86%E5%8A%A1%22%2C%22types%221%2C%22isPayBefore%221%2C%22businessUserType%22'bull'%2C%22businessCompanyName%22'bull'%2C%22isBusinessUser%22'bull'}; qlm_newbie_task=0; __jsluid_h=10ad9c18af64143065cf289c40fb00a5",
    #     "Host": "search.vip.qianlima.com",
    #     "Upgrade-Insecure-Requests": "1",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    # }
    #
    # payload = {"latestTenderType": 0, "currentPage": 1, "numPerPage": 20, "newAreaIds": "2703", "infoType": "0,1,2,3,4",
    #            "timeType": 8}
    #
    # response = requests.post(url, headers=headers)
    # # response = requests.post(url,data=payload,headers=headers)
    # print(response.text)
    pass

