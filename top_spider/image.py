import execjs
import requests


def get_js_function():
    """
    获取指定目录下的js代码, 并且指定js代码中函数的名字以及函数的参数。
    :param js_path: js代码的位置
    :param func_name: js代码中函数的名字
    :param func_args: js代码中函数的参数
    :return: 返回调用js函数的结果
    """
    with open('test.js', encoding='utf-8') as fp:
        js = fp.read()
        ctx = execjs.compile(js)
        return ctx.call('getpwd', 'szy6800+')



def get_encrypt_data():
    session = requests.session()
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        "origin": "https://mp.weixin.qq.com",
        "referer": "https://mp.weixin.qq.com/",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",

    }

    url = 'https://mp.weixin.qq.com/cgi-bin/bizlogin?action=startlogin'
    data = {
        "username": "1198558613@qq.com",
        "pwd": get_js_function(),
        "imgcode": "",
        "f": "json",
        "userlang": "zh_CN",
        'redirect_url':'',
        'token':'',
        "lang": "zh_CN",
        "ajax": "1",
    }
    res1 = session.post(url=url, headers=headers, data=data).text
    import re
    try:
        url = re.findall("/cgi-bin/home.*",res1)[0].replace('"}','')
        test = 'https://mp.weixin.qq.com'+url

        res = session.get(test)
        with open('login_result.html','wb') as f:
            f.write(res.content)
    except:
        print('发生错误')

get_encrypt_data()


