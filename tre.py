# list1 = [1,2,3,4]
# res = lambda list1:x**x
import re

a = 'not 404 found 张三 99 深圳 '
str = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", a).strip()
print(str)
