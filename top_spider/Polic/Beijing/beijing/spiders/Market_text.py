
#小行业
def index():
    cates = [
        #每页14
        {"cate": "zwxx/ttgg/", "pages": 1},#通知
        {"cate": "zwxx/zcwj/gfxwj/", "pages": 1},  # 规范性文件
        {"cate": "zwxx/zcwj/qtwj/", "pages": 1},  # 其他文件
        {"cate": "zwxx/zcjd/", "pages": 1},#政策解读
        {"cate": "zwxx/gs/cpzlgs/", "pages": 1},#产品质量公示
        {"cate": "zwxx/gs/spzlgs/", "pages": 1},#食品监督公示
        {"cate": "zwxx/gs/zhxxzx/", "pages": 1},#召回信息
        {"cate": "zwxx/gs/zxgs/", "pages": 1},#注销公示
        {"cate": "zwxx/gs/xzfysdgg/", "pages": 1},# 送达公告
        {"cate": "zwxx/gs/gycpscxkzgg/", "pages": 1},#工业产品生产许可证公告
        {"cate": "zwxx/gs/dfbzgg/", "pages": 1},#地方标准公告
        {"cate": "zwxx/gs/ggjcbg/", "pages": 1},#广告监测报告
        {"cate": "zwxx/gs/qtgsgg/", "pages": 1},#其他公示公告
        # {"cate": "bsfw/wsbs/gfdjzc/", "pages": 1},#注册登记
        {"cate": "bsfw/wsbs/gftzsb/", "pages": 1},#特种设备
        {"cate": "bsfw/bmfw/djzc/tsdj/", "pages": 1},#提示登记
        {"cate": "bsfw/bgxz/bgdjzc/", "pages": 1},#其他公示公告
        {"cate": "bsfw/bmfw/qynbbm/dbjgnbgs/", "pages": 1},  # 代表机构年报公示
        {"cate": "bsfw/bmfw/qynbbm/qynbgsbm/", "pages": 1},#企业年报公示
        {"cate": "bsfw/bmfw/dcdydjbm/", "pages": 1},#动产抵押登记
        {"cate": "bsfw/bmfw/sfwbbm/shxfl/dx/", "pages": 1},#示范文本 > 生活消费类 > 电信
        {"cate": "bsfw/bmfw/sfwbbm/shxfl/fw/", "pages": 1},#示范文本 > 生活消费类 > 房屋
        {"cate": "bsfw/bmfw/sfwbbm/shxfl/ly/", "pages": 1},#示范文本 > 生活消费类 > 旅游
        {"cate": "bsfw/bmfw/sfwbbm/shxfl/qc/", "pages": 1},#示范文本 > 生活消费类 > 汽车
        {"cate": "bsfw/bmfw/sfwbbm/shxfl/zx/", "pages": 1},#示范文本 > 生活消费类 > 装修
        {"cate": "bsfw/bmfw/sfwbbm/shxfl/qtwb/", "pages": 1},#示范文本 > 生活消费类 > 其他
        {"cate": "bsfw/bmfw/sfwbbm/nznyl/", "pages": 1},#示范文本 > 农资农业类
        {"cate": "bsfw/bmfw/sfwbbm/scjyl/", "pages": 1},#示范文本 > 生产经营类
        {"cate": "bsfw/bmfw/sfwbbm/jzgcl/", "pages": 1},# 示范文本 > 建筑工程类
        {"cate": "bsfw/bmfw/sfwbbm/spaql/", "pages": 1},#示范文本 > 食品安全类
        {"cate": "bsfw/bmfw/gzbz/", "pages": 1},# 工作标准
        {"cate": "bsfw/bmfw/bzhzl/dfbz/dfbzglbf/", "pages": 1},# 地方标准 > 地方标准管理办法
        {"cate": "bsfw/bmfw/bzhzl/dfbz/dfbzgg/", "pages": 1},# 地方标准 > 地方标准公告
        {"cate": "bsfw/bmfw/bzhzl/dfbz/dfbzjh/", "pages": 1},# 地方标准 > 地方标准计划
        {"cate": "bsfw/bmfw/bzhzl/dfbz/bzssqkbg/", "pages": 1},# 地方标准 > 标准实施情况报告
        {"cate": "bsfw/bmfw/bzhzl/bzhjswyh/tzggwyh/", "pages": 1},# 标准化 > 标准化技术委员会 > 通知公告
        {"cate": "bsfw/bmfw/bzhzl/bzhjswyh/glbfwyh/", "pages": 1},# 标准化 > 标准化技术委员会 > 管理办法
        {"cate": "bsfw/bmfw/bzhzl/bzhjswyh/ml/", "pages": 1},# 标准化技术委员会 > 名录
        {"cate": "bsfw/bmfw/bzhzl/bzzxdbz/glbfxdbz/", "pages": 1},# 标准化 > 标准化补助 > 管理办法
        {"cate": "bsfw/bmfw/bzhzl/bzzxdbz/tzggxdbz/", "pages": 1},# 标准化 > 标准化补助 > 通知公告
        {"cate": "bsfw/bmfw/bzhzl/bzzxdbz/bzjg/", "pages": 1},#  标准化补助 > 补助结果

        {"cate": "bsfw/bmfw/bzhzl/bzhsdsf/glbf/", "pages": 1},#   标准化 > 标准化试点示范 > 管理办法
        {"cate": "bsfw/bmfw/bzhzl/bzhsdsf/tzgg/", "pages": 1},#  标准化 > 标准化试点示范 > 通知公告

        {"cate": "bsfw/bmfw/gyscxkz/gzbzxkz/", "pages": 1},#  工业生产许可证 > 工作标准
        {"cate": "bsfw/bmfw/gyscxkz/tzggxkz/", "pages": 1},#  工业生产许可证 > 通知公告
        {"cate": "bsfw/bmfw/gyscxkz/xgfgwj/", "pages": 1},#  工业生产许可证 > 相关法规文件

        {"cate": "bsfw/bmfw/gyscxkz/hzqycx/", "pages": 1},#  工业生产许可证 > 获证企业查询
        {"cate": "bsfw/bmfw/gyscxkz/ndzcbg/", "pages": 1},#  工业生产许可证 > 年度自查报告
        {"cate": "bsfw/bmfw/gyscxkz/ccgg/", "pages": 1},#  工业生产许可证 >  查处公告
        {"cate": "bsfw/bmfw/gyscxkz/sywd/", "pages": 1},#  工业生产许可证 >  实用问答

        {"cate": "bsfw/bmfw/bjspqybzbazn/zxwd/", "pages": 1},#  保健食品企业标准备案指南 > 咨询问答
        {"cate": "bsfw/bmfw/bjspqybzbazn/qybzba/", "pages": 1},#  保健食品企业标准备案指南 > 企业标准备案
        {"cate": "bsfw/bmfw/xzfyxzpc/xzfy/", "pages": 1},#  行政复议、行政赔偿 > 行政复议
        {"cate": "bsfw/bmfw/xzfyxzpc/xzpc/", "pages": 1},#  行政复议、行政赔偿 > 行政赔偿

        {"cate": "hdjl/myzj/ywgzyjzj/", "pages": 1},# 意见公告
        {"cate": "hdjl/myzj/bzzxdyjzj/", "pages": 1},# 标准制修订意见征集
        {"cate": "hdjl/myzj/yjzjjg/", "pages": 1},# 意见征集结果
        {"cate": "ztzl/qybz/zcfgbz/", "pages": 1},# 法规
        {"cate": "cxfw/flfgcxfw/", "pages": 1},# 查询服务 > 法律法规
        {"cate": "zwxx/ghjh/", "pages": 1},# 政务公开 > 规划计划
        {"cate": "zwxx/zdlyzwgk/ssj/", "pages": 1},# 重点领域政务公开 > 行政执法检查“双随机”
        {"cate": "zwxx/cwxx/", "pages": 1},# 政务公开 > 财务信息
        {"cate": "zwxx/scjgdt/", "pages": 1},# 政务公开 > 动态
    ]

    # cates = [
    #     #每页14
    #             # {"cate": "zwxx/ttgg/", "pages": 19},#通知
    #             # {"cate": "zwxx/zcwj/gfxwj/", "pages": 3},  # 规范性文件
    #             # {"cate": "zwxx/zcwj/qtwj/", "pages": 12},  # 其他文件
    #             # {"cate": "zwxx/zcjd/", "pages": 9},#政策解读
    #             # {"cate": "zwxx/gs/cpzlgs/", "pages": 67},#产品质量公示
    #             # {"cate": "zwxx/gs/spzlgs/", "pages": 21},#食品监督公示
    #             # {"cate": "zwxx/gs/zhxxzx/", "pages": 8},#召回信息
    #             # {"cate": "zwxx/gs/zxgs/", "pages": 7},#注销公示
    #             # {"cate": "zwxx/gs/xzfysdgg/", "pages": 9},# 送达公告
    #             # {"cate": "zwxx/gs/gycpscxkzgg/", "pages": 3},#工业产品生产许可证公告
    #             # {"cate": "zwxx/gs/dfbzgg/", "pages": 10},#地方标准公告
    #             # {"cate": "zwxx/gs/ggjcbg/", "pages": 4},#广告监测报告
    #             # {"cate": "zwxx/gs/qtgsgg/", "pages": 7},#其他公示公告
    #             # {"cate": "bsfw/wsbs/gfdjzc/", "pages": 7},#注册登记
    #             # {"cate": "bsfw/wsbs/gftzsb/", "pages": 1},#特种设备
    #             # {"cate": "bsfw/bmfw/djzc/tsdj/", "pages": 1},#提示登记
    #             # {"cate": "bsfw/bgxz/bgdjzc/", "pages": 9},#其他公示公告
    #             # {"cate": "bsfw/bmfw/qynbbm/dbjgnbgs/", "pages": 1},  # 代表机构年报公示
    #             # {"cate": "bsfw/bmfw/qynbbm/qynbgsbm/", "pages": 2},#企业年报公示
    #             # {"cate": "bsfw/bmfw/dcdydjbm/", "pages": 1},#动产抵押登记
    #             # {"cate": "bsfw/bmfw/sfwbbm/shxfl/dx/", "pages": 1},#示范文本 > 生活消费类 > 电信
    #             # {"cate": "bsfw/bmfw/sfwbbm/shxfl/fw/", "pages": 2},#示范文本 > 生活消费类 > 房屋
    #             # {"cate": "bsfw/bmfw/sfwbbm/shxfl/ly/", "pages": 1},#示范文本 > 生活消费类 > 旅游
    #             # {"cate": "bsfw/bmfw/sfwbbm/shxfl/qc/", "pages": 2},#示范文本 > 生活消费类 > 汽车
    #             # {"cate": "bsfw/bmfw/sfwbbm/shxfl/zx/", "pages": 1},#示范文本 > 生活消费类 > 装修
    #             # {"cate": "bsfw/bmfw/sfwbbm/shxfl/qtwb/", "pages": 2},#示范文本 > 生活消费类 > 其他
    #             # {"cate": "bsfw/bmfw/sfwbbm/nznyl/", "pages": 2},#示范文本 > 农资农业类
    #             # {"cate": "bsfw/bmfw/sfwbbm/scjyl/", "pages": 2},#示范文本 > 生产经营类
    #             # {"cate": "bsfw/bmfw/sfwbbm/jzgcl/", "pages": 2},# 示范文本 > 建筑工程类
    #             # {"cate": "bsfw/bmfw/sfwbbm/spaql/", "pages": 2},#示范文本 > 食品安全类
    #             # {"cate": "bsfw/bmfw/gzbz/", "pages": 2},# 工作标准
    #             # {"cate": "bsfw/bmfw/bzhzl/dfbz/dfbzglbf/", "pages": 1},# 地方标准 > 地方标准管理办法
    #             # {"cate": "bsfw/bmfw/bzhzl/dfbz/dfbzgg/", "pages": 17},# 地方标准 > 地方标准公告
    #             # {"cate": "bsfw/bmfw/bzhzl/dfbz/dfbzjh/", "pages": 4},# 地方标准 > 地方标准计划
    #             # {"cate": "bsfw/bmfw/bzhzl/dfbz/bzssqkbg/", "pages": 1},# 地方标准 > 标准实施情况报告
    #             # {"cate": "bsfw/bmfw/bzhzl/bzhjswyh/tzggwyh/", "pages": 4},# 标准化 > 标准化技术委员会 > 通知公告
    #             # {"cate": "bsfw/bmfw/bzhzl/bzhjswyh/glbfwyh/", "pages": 1},# 标准化 > 标准化技术委员会 > 管理办法
    #             # {"cate": "bsfw/bmfw/bzhzl/bzhjswyh/ml/", "pages": 1},# 标准化技术委员会 > 名录
    #             # {"cate": "bsfw/bmfw/bzhzl/bzzxdbz/glbfxdbz/", "pages": 1},# 标准化 > 标准化补助 > 管理办法
    #             # {"cate": "bsfw/bmfw/bzhzl/bzzxdbz/tzggxdbz/", "pages": 1},# 标准化 > 标准化补助 > 通知公告
    #             # {"cate": "bsfw/bmfw/bzhzl/bzzxdbz/bzjg/", "pages": 1},#  标准化补助 > 补助结果
    #             #
    #             # {"cate": "bsfw/bmfw/bzhzl/bzhsdsf/glbf/", "pages": 1},#   标准化 > 标准化试点示范 > 管理办法
    #             # {"cate": "bsfw/bmfw/bzhzl/bzhsdsf/tzgg/", "pages": 4},#  标准化 > 标准化试点示范 > 通知公告
    #             #
    #             # {"cate": "bsfw/bmfw/gyscxkz/gzbzxkz/", "pages": 1},#  工业生产许可证 > 工作标准
    #             # {"cate": "bsfw/bmfw/gyscxkz/tzggxkz/", "pages": 3},#  工业生产许可证 > 通知公告
    #             # {"cate": "bsfw/bmfw/gyscxkz/xgfgwj/", "pages": 2},#  工业生产许可证 > 相关法规文件

    #             # {"cate": "bsfw/bmfw/gyscxkz/hzqycx/", "pages": 33},#  工业生产许可证 > 获证企业查询
    #             # {"cate": "bsfw/bmfw/gyscxkz/ndzcbg/", "pages": 1},#  工业生产许可证 > 年度自查报告
    #             # {"cate": "bsfw/bmfw/gyscxkz/ccgg/", "pages": 1},#  工业生产许可证 >  查处公告
    #             # {"cate": "bsfw/bmfw/gyscxkz/sywd/", "pages": 8},#  工业生产许可证 >  实用问答
    #             #
    #             # {"cate": "bsfw/bmfw/bjspqybzbazn/zxwd/", "pages": 1},#  保健食品企业标准备案指南 > 咨询问答
    #             # {"cate": "bsfw/bmfw/bjspqybzbazn/qybzba/", "pages": 1},#  保健食品企业标准备案指南 > 企业标准备案
    #             # {"cate": "bsfw/bmfw/xzfyxzpc/xzfy/", "pages": 1},#  行政复议、行政赔偿 > 行政复议
    #             # {"cate": "bsfw/bmfw/xzfyxzpc/xzpc/", "pages": 1},#  行政复议、行政赔偿 > 行政赔偿
    #             #
    #             # {"cate": "hdjl/myzj/ywgzyjzj/", "pages": 7},# 意见公告
    #             # {"cate": "hdjl/myzj/bzzxdyjzj/", "pages": 13},# 标准制修订意见征集
    #             # {"cate": "hdjl/myzj/yjzjjg/", "pages": 3},# 意见征集结果
    #             # {"cate": "ztzl/qybz/zcfgbz/", "pages": 4},# 法规
    #             # {"cate": "cxfw/flfgcxfw/", "pages": 26},# 查询服务 > 法律法规
    #             # {"cate": "zwxx/ghjh/", "pages": 7},# 政务公开 > 规划计划
    #             # {"cate": "zwxx/zdlyzwgk/ssj/", "pages": 2},# 重点领域政务公开 > 行政执法检查“双随机”
    #             # {"cate": "zwxx/cwxx/", "pages": 8},# 政务公开 > 财务信息
    #             # {"cate": "zwxx/scjgdt/", "pages": 6},# 政务公开 > 动态
    #         ]
    return cates
#分类

def type_polic(item):
    if '解读' in item['title']:
        item['typeId'] = 3
    elif '通告' in item['title']:
        item['typeId'] = 2
    elif '公示' in item['title']:
        item['typeId'] = 2
    elif '公告' in item['title']:
        item['typeId'] = 2
    elif '通知' in item['title']:
        item['typeId'] = 1
    elif '服务' in item['title']:
        item['typeId'] = 4
    elif '指南' in item['title']:
        item['typeId'] = 4
    elif '？' in item['title']:
        item['typeId'] = 4
    elif '法' in item['title']:
        item['typeId'] = 5
    elif '条例' in item['title']:
        item['typeId'] = 5
    else:
        item['typeId'] = 1

    return item['typeId']










