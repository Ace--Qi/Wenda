# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import  Request
from tutorial.items import DmozItem
class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["zhidao.baidu.com"]
    def parse(self, response):
           #item = DmozItem()
           title=response.xpath('//div[@id="wgt-list"]/dl[1]/dt/a/@href').extract()
           s = str(title).replace('u\'', '')
           a = s.decode("unicode-escape").encode("utf-8")
           a = a.split('[')[1].split("']")[0]
           print "执行爬虫"
           yield Request(url=a, callback=self.parse_item)
           '''
            title=response.xpath('//title/text()').extract()
            s = str(title).replace('u\'', '')
            a = s.decode("unicode-escape").encode("utf-8")
            a = a.split('_')[0].split('[')[1]
            item['title'] =a
            print a
            link = response.xpath('//meta[@name="description"]/@content').extract()
            s = str(link).replace('u\'', '')
            a = s.decode("unicode-escape").encode("utf-8")
            a = a.split('[')[1].split("']")[0]
            item['link'] = a
            print a
            '''


    def parse_item(self, response):
        item = DmozItem()
        message={}
        title = response.xpath('//title/text()').extract()
        s = str(title).replace('u\'', '')
        a = s.decode("unicode-escape").encode("utf-8")
        a = a.split('_')[0].split('[')[1]
        item['title'] = a
        message["title"]=item['title']
        link = response.xpath('//meta[@name="description"]/@content').extract()
        s = str(link).replace('u\'', '')
        a = s.decode("unicode-escape").encode("utf-8")
        a = a.split('[')[1].split("']")[0]
        item['link'] = a
        message["answer"] = item['link']
        desc = response.xpath('//pre[@class="best-text mb-10"]//text()').extract();
        s = str(desc).replace('u\'', '').replace("\u3000",'')
        a = s.decode("unicode-escape").encode("utf-8")
        a = a.replace('[', '')
        a = a.replace("',", '')
        a = a.replace("'", '')
        a = a.replace("]", '')
        if a =="":
            desc = response.xpath('//div[@class="answer-text mb-10"]/p//text()').extract();
            s = str(desc).replace('u\'', '').replace("\u3000",'')
            a = s.decode("unicode-escape").encode("utf-8")
            a = a.replace('[','')
            a = a.replace("',", '')
            a = a.replace("'", '')
            a = a.replace("]", '')
        if a=="":
            desc = response.xpath('//div[@class="best-text mb-10"]/p//text()').extract();
            s = str(desc).replace('u\'', '').replace("\u3000",'')
            a = s.decode("unicode-escape").encode("utf-8")
            a = a.replace('[', '')
            a = a.replace("',", '')
            a = a.replace("'", '')
            a = a.replace("]", '')
        item['desc'] = a
        message["desc"]=item['desc']
        # populate `item` fields
        print "写入item文件"
        with open("/Users/wangqi/PycharmProjects/wenda/tutorial/items.json", "w") as f:
            json.dump(message, f,sort_keys=True, indent=2,ensure_ascii=False)
        f.close()
        return item
