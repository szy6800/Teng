"""有道翻译整体思路：
1.首先找到翻译的请求与传递地址：https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule
    第一、其中具有的返回数据如下：
        "translateResult": [
        [
            {
                "tgt": "苹果",
                "src": "apple"
            }
        ]
        输入的数据是apple 返回的翻译结果 苹果 我们想要的数据就存在这组json数据格式的 ['translateResult'][0]['tgt']中
    第二、查看此URL的请求参数，找到是以那些请求头参数向网页传入的需要翻译的内容。
          headers = {
            "i": "apple",
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": "16555291396783",   -->加密参数（可能是时间戳）
            "sign": "d2a2e590151a473a253adbd2fbb3adcb",   -->加密参数
            "lts": "1655529139678",   -->加密参数（可能是时间戳）
            "bv": "09e377475805a2fb71b566de21e0dc2b",   -->加密参数
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME"
            }
    2.对整体的分析完毕，进行请求头参数加密的js逆向，寻找当前页面用什么方式进行的加密。
    首先是整体的参数生成的js函数代码：
     t.translate = function(e, t) {
        k = f("#language").val();
        var n = w.val()
          , r = v.generateSaltSign(n)
          , i = n.length;
        if (M(),
        _.text(i),
        i > 5e3) {
            var o = n;
            n = o.substr(0, 5e3),
            r = v.generateSaltSign(n);
            var s = o.substr(5e3);
            s = (s = s.trim()).substr(0, 3),
            f("#inputTargetError").text("有道翻译字数限制为5000字，“" + s + "”及其后面没有被翻译!").show(),
            _.addClass("fonts__overed")
        } else
            _.removeClass("fonts__overed"),
            f("#inputTargetError").hide();
        p.isWeb(n) ? a() : c({
            i: n,
            from: C,
            to: S,
            smartresult: "dict",
            client: E,
            salt: r.salt,
            sign: r.sign,
            lts: r.ts,
            bv: r.bv,
            doctype: "json",
            version: "2.1",
            keyfrom: "fanyi.web",
            action: e || "FY_BY_DEFAULT"
        }, t)
    }
    可以看到大部分的参数都是通过使用r这个函数来生成的，r这个函数使用的是r = v.generateSaltSign(n);
    接下来找r = v.generateSaltSign(n);这个js的代码部分：这是讲n传入给了这个r函数，所以n 在开头可以分析到是我们写入的需要翻译的字符串
    var r = function(e) { -->传入的e也是字符串
        var t = n.md5(navigator.appVersion)
          , r = "" + (new Date).getTime()     ---> r在这里获取了时间，是时间戳
          , i = r + parseInt(10 * Math.random(), 10);   --> i 是 时间戳 + 一个随机的整数，在0-9之间
        return {
            ts: r,  -->时间戳
            bv: t,  --> bv就是t 而t来自于上面的赋值 调用n.md5对浏览器信息进行假买，也就是对：5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44 进行md5加密
            salt: i,    --> 时间戳 + 一个随机的整数，在0-9之间
            sign: n.md5("fanyideskweb" + e + i + "Ygy_4c=r#e#4EX^NUGUc5")  --> 签名加密的所在之处 "fanyideskweb" + e + i + "Ygy_4c=r#e#4EX^NUGUc5"采用md5加密算法
        }                                                                                               这里e 是这个r函数传进来的参数，去找个这个参数，发现是我们需要翻译的字符串
    };                                                                                                     i是前面分析的时间戳 + 一个随机的整数，在0-9之间
    t.recordUpdate = function(e) {
        var t = e.i
          , i = r(t);
        n.ajax({
            type: "POST",
            contentType: "application/x-www-form-urlencoded; charset=UTF-8",
            url: "/bettertranslation",
            data: {
                i: e.i,
                client: "fanyideskweb",
                salt: i.salt,
                sign: i.sign,
                lts: i.ts,
                bv: i.bv,
                tgt: e.tgt,
                modifiedTgt: e.modifiedTgt,
                from: e.from,
                to: e.to
            },
            success: function(e) {},
            error: function(e) {}
        })
    3.得到的结果：
        bv = 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44 md5加密
        salt = 时间戳 + 一个随机的整数，在0-9之间
        sign = "fanyideskweb" + 我们输入的需要翻译的内容 + salt + "Ygy_4c=r#e#4EX^NUGUc5" md5加密
        lts = 时间戳
        最终：
        headers = {
            "i": "我们输入的字符串",
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": 时间戳 + 一个随机的整数，在0-9之间
            "sign": "fanyideskweb" + 我们输入的字符串 + salt + "Ygy_4c=r#e#4EX^NUGUc5" md5加密
            "lts": 时间戳
            "bv": 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44 md5加密
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME"
        }
"""
import time
import requests
from random import randint
from hashlib import md5


class youdao(object):
    def __init__(self):
        self.url = "https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

    def md5_encrypt(self, content):
        hl = md5()
        hl.update(content.encode(encoding='utf-8'))
        return hl.hexdigest()

    def spider(self,keys):
        # 获取当前时间（取整再转字符串）用来获取lts参数
        ts = str(int(time.time() * 1000))
        lts = ts

        # 设置salt参数（时间戳+随机0-9的整数）
        salt = lts + str(randint(0, 9))

        # 设置sign参数（"fanyideskweb" + 我们输入的字符串 + salt + "Ygy_4c=r#e#4EX^NUGUc5" md5加密）
        sign = self.md5_encrypt("fanyideskweb" + keys + salt + "Ygy_4c=r#e#4EX^NUGUc5")
        headers = {
            "Cookie": "OUTFOX_SEARCH_USER_ID=-1883290551@10.110.96.158; OUTFOX_SEARCH_USER_ID_NCOO=1303558223.335795; fanyi-ad-id=306808; fanyi-ad-closed=1; ___rl__test__cookies={}".format(ts),
            "Host": "fanyi.youdao.com",
            "Origin": "https://fanyi.youdao.com",
            "Referer": "https://fanyi.youdao.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44",
        }

        bv = self.md5_encrypt(headers['User-Agent'])
        params = {
            "i": keys,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "lts": ts,
            "bv": bv,
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlM"
        }
        resp = requests.post(url=self.url, data=params, headers=headers).json()
        # print(resp)
        if resp['errorCode'] == 0:
            result = resp['translateResult'][0][0]['tgt']
            print(f'翻译的结果是：{result}')
        elif resp['errorCode'] == 40:
            print('此语种未被识别！')


def run():
    translate = youdao()
    while True:
        keys = input('请输入想要翻译的内容（按Y退出）：')
        if keys == 'y':
            break
        else:
            translate.spider(keys)

if __name__ == '__main__':
    run()
