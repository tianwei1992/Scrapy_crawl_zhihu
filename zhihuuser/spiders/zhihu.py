# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json

from zhihuuser.items import UserItem
#自定义的类也要引入

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    start_user = 'gao-ke-69'

    user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), self.parse_user)
        yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query, limit=20, offset=0),
                      self.parse_follows)
        yield Request(self.followers_url.format(user=self.start_user, include=self.followers_query, limit=20, offset=0),
                      self.parse_followers)


    def parse_user(self, response):
        print('parse_user')
        data=json.loads(response.text)#json格式反序列化
        item=UserItem()
        for field in item.fields:#item.fields列出item的所有的属性
            if field in data.keys():#如果我们想要的字段，确实爬到了相应的数据，就用它填充
                item[field]=data.get(field)
        yield item
        # yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query, limit=20, offset=0),
        #               self.parse_follows)
        # yield Request(self.followers_url.format(user=self.start_user, include=self.followers_query, limit=20, offset=0),
        #               self.parse_followers)

    def parse_follows(self,response):

        print('parse_follows')
        data = json.loads(response.text)  # json格式反序列化
        if 'data' in data.keys():#有关注的人，才有data字段
            for follow in data.get('data'):
                url_token=follow.get('url_token')
                yield Request(self.user_url.format(user=url_token, include=self.user_query), self.parse_user)
        if 'paging' in data.keys() and data.get('paging').get('is_end')==False:
            yield Request(data.get('paging').get('next'),self.parse_follows)

    def parse_followers(self,response):
        print('parse_follower')
        data = json.loads(response.text)  # json格式反序列化
        if 'data' in data.keys():#有关注者，才有data字段
            for follower in data.get('data'):
                url_token=follower.get('url_token')
                yield Request(self.user_url.format(user=url_token, include=self.user_query), callback=self.parse_user)
        if 'paging' in data.keys() and data.get('paging').get('is_end')==False:
            yield Request(data.get('paging').get('next'),callback=self.parse_followers)




