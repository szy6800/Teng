# coding:utf-8
a = '''

'''
import re

b = re.findall('来源[:： \n]+(.*?)<', a)[0]
print(b)


# b = re.findall('\d{2}/\d{2}', a)


