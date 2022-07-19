# coding:utf-8
a = '''
    “我一直关心新疆的建设发展”——记习近平总书记在新疆考察
      </h1>
      <div class="pages-date">2022-07-17 07:50  <span class="font">来源： 新华社</span>
      <div class="pages_print"><span class="font index_switchsize">【字体：<span class="bigger">大</span> <span class="medium">中</span> <span class="smaller">小</span>】</span><span style="cursor:pointer;" class="font printIco" onclick="javascript:window.print()">打印</span>
 <!-- share -->
        <div class="share" id="share">
          <div class="share-icon"></div>
'''
import re

b = re.findall('来源[:： \n]+(.*?)<', a)[0]
# print(b)


n = '018'
print("{:0<d}".format(int(n)))
# b = re.findall('\d{2}/\d{2}', a)


