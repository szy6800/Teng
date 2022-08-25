# -*- coding: utf-8 -*-
import json

import jsonpath
import scrapy


class CommentSpider(scrapy.Spider):
    name = 'comment'
    allowed_domains = ['video.kuaishou.com']
    # start_urls = ['https://video.kuaishou.com/short-video/3xpde7ajycw38ra?authorId=3xcuaxnya25pnb4&streamSource=search&searchKey=%E7%BA%B3%E7%A8%8E&area=searchxxnull']

    def start_requests(self):
        # 构建url

        # 构建post请求参数
        data = {"operationName":"commentListQuery","variables":{"photoId":"3xzwugqxpna5m5g","pcursor":""},"query":"query commentListQuery($photoId: String, $pcursor: String) {\n  visionCommentList(photoId: $photoId, pcursor: $pcursor) {\n    commentCount\n    pcursor\n    rootComments {\n      commentId\n      authorId\n      authorName\n      content\n      headurl\n      timestamp\n      likedCount\n      realLikedCount\n      liked\n      status\n      subCommentCount\n      subCommentsPcursor\n      subComments {\n        commentId\n        authorId\n        authorName\n        content\n        headurl\n        timestamp\n        likedCount\n        realLikedCount\n        liked\n        status\n        replyToUserName\n        replyTo\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
        # 发送post请求
        yield scrapy.FormRequest(
            url = 'https://video.kuaishou.com/graphql',
            method='POST',
            body=json.dumps(data),
            headers={'Content-Type': 'application/json'},
            encoding='gbk',
            callback=self.parse)

    def parse(self,response):
        item = {}
        text = json.loads(response.text)
        # print(text)
        list_url = jsonpath.jsonpath(text, '$..content')
        # comment = text['data']['visionCommentList']['rootComments']
        for i in list_url:
            item['comment'] = i
            yield item

