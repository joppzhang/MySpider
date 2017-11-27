import scrapy

import re

import urllib

from ..items import MymoviesSpiderItem

class movie_spider(scrapy.Spider):
    name = "comedy"
    allowed_domains = ["www.87movie.com"]
    start_urls = ["http://www.87movie.com/tag/%E5%96%9C%E5%89%A7/"]

    def parse(self, response):
        num_page = response.xpath(
            "/html/body/div[1]/div/div/div[2]/div/nav/ul/li[7]/a/@href").extract()
        number = 1
        if len(num_page) > 0:
            number = int(num_page[0].split('/')[-1].split('?')[0])
        for i in range(1, number + 1):
            yield scrapy.Request(response.url + str(i) + '?o=data',callback=self.parse_page )

    def parse_page(self, response):
        print("调用了prase_page函数")
        movies = response.xpath('/html/body/div[1]/div/div/div[2]/div/ul/li[2]/div/div[2]/h4/a/@href').extract()#进入电影列表页之后，获取电影的链接
        url_host = 'http://' + response.url.split('/')[2]#获取url的头部信息
        for i in movies:
            movie_info=MymoviesSpiderItem()
            yield scrapy.Request(url_host+i,meta={'movie_info':movie_info},callback=self.parse_detail)

    def parse_detail(self,response):
        movie_info = response.meta['movie_info']
        movie_info['name'] = response.xpath('//div[@class="white-div"]//h3/text()').extract()
        movie_info['pic'] = response.xpath('//div[@class="white-div"]//img/@src').extract()
        movie_info['content'] = response.xpath('//div[@class="white-div"]//div[@class="col-md-8"]/text()').extract()
        movie_info['download'] = response.xpath('//div[@id="down1"]/div[@class="panel-body"]/ul/li/a/@href').extract()
        return movie_info#最外层函数，直接return数据

