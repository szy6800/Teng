a = '''
<span class="times">
发布时间：2022-07-07
</span>
<span class="author">
来源：国家能源局
</span>
<span class="switchsize"><b class="bigger">大</b><b class="medium">中</b><b class="smaller">小</b></span>
<div class="arrow"></div>
'''
import re
b = re.findall('来源[:： \n]+(.*?)[\n]',a)
print(b)