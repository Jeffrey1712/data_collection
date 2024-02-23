import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

class imdb_spider(scrapy.Spider):

    name = "imdb"

    start_urls = [
        'https://www.imdb.com/chart/top',
    ]

    def parse(self, response):
        n = 250
        for i in range(n):
            i = i + 1
            yield {
                "duration": response.xpath('/html/body/div[2]/main/div/div[3]/section/div/div[2]/div/ul/li[{}]/div[2]/div/div/div[2]/span[2]/text()'.format(i)).get(),
                "ranking": response.xpath('/html/body/div[2]/main/div/div[3]/section/div/div[2]/div/ul/li[{}]/div[2]/div/div/div[1]/a/h3/text()'.format(i)).get().split(".")[0],
                "title": response.xpath('/html/body/div[2]/main/div/div[3]/section/div/div[2]/div/ul/li[{}]/div[2]/div/div/div[1]/a/h3/text()'.format(i)).get().split(".")[1], 
                "url": response.xpath('/html/body/div[2]/main/div/div[3]/section/div/div[2]/div/ul/li[{}]/div[2]/div/div/div[1]/a'.format(i)).attrib["href"],
                "rating":response.xpath('/html/body/div[2]/main/div/div[3]/section/div/div[2]/div/ul/li[{}]/div[2]/div/div/span/div/span/text()'.format(i)).get(),
                'year': response.xpath('/html/body/div[2]/main/div/div[3]/section/div/div[2]/div/ul/li[{}]/div[2]/div/div/div[2]/span[1]/text()'.format(i)).get()
            }
filename = "imdb2.json"

if filename in os.listdir('test/'):
        os.remove('test/' + filename)

process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'test/' + filename : {"format": "json"},
    }
})

process.crawl(imdb_spider)
process.start()

#rajouter du code python parser le code json et le transformer en DataFrame