# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

from maoyan_info.items import MaoyanInfoItem
from scrapy import Selector

from scrapy.http import Request


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    pagelist = [7, 6, 1, 2, 4]

    def start_requests(self):
        for i in self.pagelist:
            self.url = 'http://maoyan.com/board/{page}'.format(page=i)


            # url = 'https://movie.douban.com/top250'
            print(self.url)
            yield Request(self.url, callback=self.parse)

    def parse(self, response):
        print('-------------------------------')
        item = MaoyanInfoItem()
        selector = Selector(response)
        movies = selector.xpath('//div[@class="movie-item-info"]')
        for i, content in enumerate(movies):
            title = content.xpath('p[@class="name"]/a/text()').extract_first()
            star = content.xpath('p[2]/text()').extract_first()
            releasetime = content.xpath('p[3]/text()').extract_first()

            item['title'] = title
            item['star'] = star.strip()
            item['time'] = releasetime

            yield item

