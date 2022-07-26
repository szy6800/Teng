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

# a = '121.50776,31.234293'
# lng = a.split(',')[0]
# lat = a.split(',')[1]
# print(lng)
# print(lat)
# # n = '018'
# # print("{:0<d}".format(int(n)))
# # b = re.findall('\d{2}/\d{2}', a)


lsp1 = '''

https://www.liepin.com/job/1951008835.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=0&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=0
https://www.liepin.com/job/1948136107.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=1&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=1
https://www.liepin.com/job/1950687669.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=2&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=2
https://www.liepin.com/a/36674601.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=3&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=3
https://www.liepin.com/job/1951384719.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=4&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=4
https://www.liepin.com/job/1951385713.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=5&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=5
https://www.liepin.com/job/1949150987.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=6&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=6
https://www.liepin.com/job/1947871283.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=7&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=7
https://www.liepin.com/job/1946461843.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=8&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=8
https://www.liepin.com/job/1945907577.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=9&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=9
https://www.liepin.com/job/1945497339.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=10&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=10
https://www.liepin.com/job/1945484301.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=11&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=11
https://www.liepin.com/job/1945484185.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=12&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=12
https://www.liepin.com/job/1945483757.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=13&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=13
https://www.liepin.com/job/1944161093.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=14&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=14
https://www.liepin.com/job/1945015513.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=15&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=15
https://www.liepin.com/job/1931681011.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=16&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=16
https://www.liepin.com/job/1951384679.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=17&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=17
https://www.liepin.com/job/1925387979.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=18&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=18
https://www.liepin.com/job/1950070677.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=19&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=19
https://www.liepin.com/job/1951054579.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=20&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=20
https://www.liepin.com/job/1951054577.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=21&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=21
https://www.liepin.com/job/1951054231.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=22&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=22
https://www.liepin.com/job/1951054229.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=23&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=23
https://www.liepin.com/job/1951054227.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=24&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=24
https://www.liepin.com/job/1950989385.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=25&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=25
https://www.liepin.com/job/1950009101.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=26&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=26
https://www.liepin.com/job/1950007397.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=27&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=27
https://www.liepin.com/job/1950007377.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=28&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=28
https://www.liepin.com/job/1950007315.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=29&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=29
https://www.liepin.com/job/1950007253.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=30&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=30
https://www.liepin.com/job/1950007243.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=31&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=31
https://www.liepin.com/job/1950007233.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=32&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=32
https://www.liepin.com/job/1950007219.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=33&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=33
https://www.liepin.com/job/1950007201.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=34&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=34
https://www.liepin.com/lptjob/51384483?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=35&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=35
https://www.liepin.com/job/1951384363.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=36&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=36
https://www.liepin.com/job/1951271273.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=37&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=37
https://www.liepin.com/job/1950787215.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=38&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=38
https://www.liepin.com/job/1950226721.shtml?d_sfrom=search_prime&d_ckId=a306550fcb71b0637f7fdaf926ec5527&d_curPage=0&d_pageSize=40&d_headId=a991cb9786418e0ba1a3b7d908e9eeee&d_posi=39&skId=ytxnph12efu96jc6qt0wj5oomcuqjpyb&fkId=1kd8f2u8s2csdkgsekybhhinier2x9w8&ckId=1kd8f2u8s2csdkgsekybhhinier2x9w8&sfrom=search_job_pc&curPage=0&pageSize=40&index=39

Process finished with exit code 0

'''
a = re.findall('https://www.liepin.com/.*?\?d',lsp1)
print(len(a))
print(a)


