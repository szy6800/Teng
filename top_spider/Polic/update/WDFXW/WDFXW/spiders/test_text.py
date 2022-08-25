
#纳税服务里的各种小分类
def index():
    cates = [

            ]
    return cates


def type_polic(item):
    # 新闻类型
    if 'cid=27' in item['list_url']:
        item['type'] = '劳务合同'
    elif 'cid=28' in item['list_url']:
        item['type'] = '劳动合同'
    elif 'cid=29' in item['list_url']:
        item['type'] = '聘用聘请合同'
    elif 'cid=30' in item['list_url']:
        item['type'] = '停薪留职合同'
    elif 'cid=31' in item['list_url']:
        item['type'] = '人事保管、挂靠合同'
    elif 'cid=32' in item['list_url']:
        item['type'] = '竞业禁止合同'
    elif 'cid=33' in item['list_url']:
        item['type'] = '借调合同'
    elif 'cid=34' in item['list_url']:
        item['type'] = '其他劳动劳务合同'
    elif 'cid=108' in item['list_url']:
        item['type'] = '集体劳动合同'
    elif 'cid=183' in item['list_url']:
        item['type'] = '员工培训合同'
    else:
        item['type'] = ''

    return item['type']












