# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs

class MymoviesSpiderPipeline(object):
    # def process_item(self, item, spider):
    #     return item

    def __init__(self):
        # 初始化函数，新建一个名为movie_info.json的文件
        self.file = codecs.open(
            'movie_info.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 这里的item参数，就是我们在items.py中定义的MovieSpiderItem，也就是爬虫函数中返回的movie_info
        # 处理函数，item['content']不是全部要，知道倒数第二个
        item['content'] = item['content'][-2]
        # item转换成json，默认转ascii编码的设置关闭
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # 这次的数据，不是保存数据库和文本文件，而是保存在json【json是非常有用的】文件中。
        self.file.write(line)
        return item # 终端会打印item信息就是因为有这句

    def spider_closed(self, spider):
        # 爬虫关闭时处理的函数，关闭文件
        self.file.close()
