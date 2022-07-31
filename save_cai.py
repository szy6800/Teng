import requests
from sele import get_cookies

# cookies = {
#
#     'GahMaMhTvKpTS': '5I2a2pOloOzvmxd9AM6.3yI_GP9RVhxh_wWPDMptfTrQp1UWv7H3KXoeL.mNI.MoyjUXs2o7RmGFcmu3wrleBiq',
#
#     'GahMaMhTvKpTT': 'Qu6mZ5dVupgn60wQ5L_tsB.ckGky7PzZNgyDLPp_Q_un.wzEFQ4GeUG2f8DDorNK5J9DGsCxpv8rQ6x5XWxlzNl3I3bxl4BEw8as0CM2btEXW.UfXUTk.vFcLJIqq0gLzfkvdsNY4uS5NMeblt8aFM.iN7S309mp6qMyh1IwvoLpE57ZNLZCLAEmVEsU_ztvlEwORHPHMiEfBxqzMvICOOht1t_58BEdp8iGeMcz.x9mxklLwt5rRQQdUt_K0mvtPcIkCefYw8lRXDbTxO8z9jAjA.Yev5awJJqyL6GCrZzKu1KG4D.qYrmtcivvb68zfSH.FzOQFIm.9dSfz4z3kRx2YcvQ.8bXTDSy0WEHWUsZaiV8u7taIOt.0hbyIq42Zz1IVGzlcz3F0Ao21DSTHA',
# }

cookies = {
    'enable_undefined': 'true',
    'GahMaMhTvKpTS':get_cookies()[0],
    '__jsluid_h': '627a525117a522418016c829c10c1d0d',
        'GahMaMhTvKpTT':get_cookies()[1],
}

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

response = requests.get('http://xdec.cnpc.com.cn/xdec/cbzbggao/common_list1_template.shtml', headers=headers, cookies=cookies, verify=False)
print(response.text)