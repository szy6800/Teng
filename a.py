# -*- coding: utf-8 -*-

# @Time : 2022/5/10 12:36
# @Author : 石张毅
# @Site : 
# @File : a.py
# @Software: PyCharm
listss = ['11','12','13']
def adds(lists):
    lists.append('a')
    return lists

print(   (map(adds(listss),listss)))

for i in listss:
    for s in enumerate(range(10)):
        print(s)