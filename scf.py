# coding:utf-8
a = '''
</div>

<div class="cinfo center">
	<span id="con_time">发布时间：2022-07-13 15:01</span>  <span>来源：离退休干部局</span>
</div>
'''

import re
b = re.findall('来源[:： \n]+(.*?)<',a)
print(b)

