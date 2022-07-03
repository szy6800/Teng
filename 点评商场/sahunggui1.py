from sqlalchemy import create_engine
import pymysql
from sqlalchemy.types import *
import numpy as np
import pandas as pd
import time
import json
from 点评商场.tools import *

def dbz(count):
 # now = datetime.datetime.now()
 # otherStyleTime = now.strftime("%Y-%m-%d")

 sql1 = f'''SELECT city,id,title,link,jsons FROM `dianping2021_shangchang` WHERE city='{count}' AND jsons!='无';'''
 sql2 = f'''SELECT city,fid as id FROM `dianping2021_dianpuid` WHERE city='{count}';'''
 # print(sql)
 engine = create_engine('mysql+pymysql://root:Lxp.138927!asd@123.126.87.123:3306/crawler2021?charset=utf8')
 engine2 = create_engine('mysql+pymysql://root:Lxp.138927!asd@123.126.87.123:3306/crawler2021?charset=utf8')
 df = pd.read_sql(sql1, engine)
 df = df.drop_duplicates(subset=['id'])  # 默认保留一条重复数据
 # print(df)
 df1 = pd.read_sql(sql2, engine2)
 print(len(df))
 print(len(df1))
 df1 = df1.drop_duplicates(subset=['id'])  # 默认保留一条重复数据
 engine.dispose()
 engine2.dispose()
 # print(df1)
 db2 = pd.concat([df, df1], axis=0, sort=False, ignore_index=True)
 # print(db2)
 dbz = db2.drop_duplicates(subset=['id'], keep=False)
 # print(dbz)
 print(f'对比保留了{len(dbz)}条')
 dbz = dbz[['city', 'id', 'title', 'link', 'jsons']].values.tolist()  # df转列表
 # print(dbz)
 return dbz

# def queryue(sql):
#     # engine = create_engine('mysql+pymysql://root:I0z>kp9tnavw@127.0.0.1:3306/crawler2021?charset=utf8')
#     engine = create_engine('mysql+pymysql://root:q!dwyyl6:q3L@127.0.0.1:3306/test?charset=utf8')
#
#     df = pd.read_sql_query(sql, engine)
#
#     lists1 = np.array(df)
#
#     lists = lists1.tolist()
#     # print(lists)
#     return lists
#
# # 模糊查询
# """SELECT * FROM meituan2 WHERE url LIKE '%fz.meituan.com%';"""
#
#
# def id_sult():
#     # sql = 'SELECT * FROM meituan1 WHERE 地市详情链接="http://nd.meituan.com/meishi"'
#     # sql = 'SELECT * FROM zhaobiao2021;'
#     sql = f"SELECT * FROM `dianping2021_shangchang` WHERE province='山西省' AND jsons!='无';"
#     result1 = queryue(sql=sql)
#     page = len(result1)
#     print(f'========读取总数>>{page}条=======')
#     # print(result1)
#     # print(result1)
#     result = []
#     for i in range(page):
#         result.append(result1[i])
#     print('=========读取完毕=========')
#     return result

def df_to_mysql(df_all, table2, db):
    df_save = df_all
    if len(df_save) >= 0:
        try:
            engine = create_engine('mysql+pymysql://root:Lxp.138927!asd@123.126.87.123:3306/{}?charset=utf8'.format(db))
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


class AddrLng():

    def __init__(self):
        # self.browser = login('')
        # self.browser.implicitly_wait(10)
        # result = id_sult()
        # df2 = pd.DataFrame(data=result)
        # df2.columns = ['province', 'city', 'county', 'district', 'analysis', 'title', 'url', 'link', 'id']
        # self.df2 = df2.drop_duplicates(subset="id")
        self.df2 = dbz('太原市')


    def start(self):
        # print(d_list)
        shangchenglist = []
        for d_list in self.df2:
            print(d_list)
            shoping_list = []
            city = d_list[0]
            uid = d_list[1]
            count_list = json.loads(d_list[-1])
            shopid = re.search('//pages/list/list\?mallId=(.*)', count_list[0]['listUrl']).group(1)
            for count in count_list[1:]:
                cateId = count['cateId']
                for t in count['tagList']:
                    tag = t['name']
                    typ = t['type']
                    time.sleep(10)
                    url = f'https://mapi.dianping.com/shopping/navipoilist?version=9.0.0&shopid={shopid}&shopIdL={shopid}&cityid=2&cateid={cateId}&tag={tag}&type={typ}'

                    headers = {
                        "Accept": "*/*",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Connection": "keep-alive",
                        "Cookie": '_lxsdk_cuid=17f6dbbd427c8-033249ccf684f3-a3e3164-fa000-17f6dbbd42730; _hc.v=53f61794-31d8-04a3-2e39-e48f068515b6.1646813501; s_ViewType=10; ua=dpuser_7142972303; ctu=732ea57f8779eb2d9394d7bd1cd9989c1b5622de45fe90c64caed66f8a76e84d; _ga=GA1.2.818741495.1652847358; uuid=8EE882A3DC138BA42FDB9A59DCC8B34B8A1C79B579386A4BE23E9D496FDA6DF0; iuuid=8EE882A3DC138BA42FDB9A59DCC8B34B8A1C79B579386A4BE23E9D496FDA6DF0; _lxsdk=8EE882A3DC138BA42FDB9A59DCC8B34B8A1C79B579386A4BE23E9D496FDA6DF0; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1656668899,1656685692,1656685733; logan_custom_report=; WEBDFPID=31883v47zv6y5vxxy305416w3v401085818yw9v7u0v9795846374911-1656820631958-1656734229606MEUIWCIfd79fef3d01d5e9aadc18ccd4d0c95072511; m_flash2=1; dper=0003c99ee936da630c4682847f62837bc16b527b124b3e8ddd7c8b96299e6648e740ced84626bd8d0b01365b9fd2b6c3ac3db6908be9fe2c2087d92100b9fb13; pvhistory=5oiR6KaB54K56K+EPjo8L3Nob3AvRzRocHhYaTBKem9wenRqdS9yZXZpZXc+OjwxNjU2NzUyNDY0NDcxXV9b; ll=7fd06e815b796be3df069dec7836c3df; csrftoken="NDEsLTEyMCwxMTksMTA5LDE4LDAsLTg5LDY0LC0yMywtMTI4LC0zOSw4OSwtMzksLTgsLTU2LC0yNg=="; Hm_lvt_233c7ef5b9b2d3d59090b5fc510a19ce=1656752510; Hm_lpvt_233c7ef5b9b2d3d59090b5fc510a19ce=1656752510; cityid=2; msource=default; chwlsource=default; Hm_lvt_220e3bf81326a8b21addc0f9c967d48d=1656752520; switchcityflashtoast=1; dp_pwa_v_=e6bedb6341239f38f06e5ac2919f181405633d25; default_ab=index%3AA%3A3%7Cmyinfo%3AA%3A1; logan_session_token=5gjafxy8aqe3hvzpzmqr; Hm_lpvt_220e3bf81326a8b21addc0f9c967d48d=1656752532; _lxsdk_s=181be150da1-cab-f79-04d%7C%7C368',
                        "Host": "mapi.dianping.com",
                        "Origin": "https://m.dianping.com",
                        "Referer": "https://m.dianping.com/",
                        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
                        "sec-ch-ua-mobile": "?1",
                        "sec-ch-ua-platform": "\"Android\"",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-site",
                        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Mobile Safari/537.36"
                    }

                    response = requests.get(url, headers=headers)
                    print(response.text)
                    respon = json.loads(response.text)
                    try:
                        cout_list = respon['msg']['list']
                        for cout in cout_list:
                            item = []
                            item.append(city)
                            item.append(uid)
                            try:
                                url = re.search('(.*?)&shoptype=',cout['jumpUrl']).group(1)
                            except:
                                url = cout['jumpUrl']
                            item.append(cout['title'])
                            item.append(url)
                            item.append(cout['shopuuid'])
                            print(item)
                            shoping_list.append(item)
                    except:
                        pass
            print('保存了')
            if shoping_list == []:
                continue
            df1 = pd.DataFrame(data=shoping_list)
            df1.columns = ['city', 'fid', 'title', 'link', 'id']
            df_to_mysql(df1, 'dianping2021_dianpuid', 'crawler2021')



                # break
            # break



            # new_url = d_list[7]
            # # new_url = 'https://m.dianping.com/shop/l2xBxMtsWIf7CezP?source=pc_jump'
            # self.browser.get(new_url)  # 详情页
            # html = self.browser.page_source.encode("utf8").decode("utf8")  # 页面转码,防止乱码数据
            # time.sleep(10)
            # # etrr = etree.HTML(html)  # 实例化页面
            # shop_list = analysis(d_list, html)
            # # print(shop_list)
            # shangchenglist.append(shop_list)
            # # break
            # print(shangchenglist)
            # if len(shangchenglist) == 50:
            #     df1 = pd.DataFrame(data=shangchenglist)
            #     df1.columns = ['province', 'city', 'county', 'district', 'analysis', 'title', 'url', 'link', 'id','jsons']
            #     df_to_mysql(df1, 'dianping2021_shangchang', 'test')
            #     shangchenglist = []



if __name__ == '__main__':
    AddrLng = AddrLng()
    AddrLng.start()