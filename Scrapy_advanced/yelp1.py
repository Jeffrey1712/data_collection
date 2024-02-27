import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

class YelpSpider(scrapy.Spider):
    # Name of your spider
    name = "yelp"

    # Starting URL
    start_urls = ['https://www.yelp.fr/']

    # Parse function for form request
    def parse(self, response):
        # FormRequest used to make a search in Paris
        # https://www.yelp.fr/search?find_desc=restaurant+japonais&find_loc=Paris
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'find_desc': 'restaurant japonais',
                'find_loc':'Paris'
                },
            callback=self.after_search
        )

    # Callback used after login
    def after_search(self, response):
            # en cliquant sur le nom de plusieurs restaus : li[1], li[2] donc li
        names = response.xpath('//*[@id="main-content"]/div/ul/li/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/div/div/h3/span/a/text()')
                               
        urls = response.xpath('//*[@id="main-content"]/div/ul/li/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div/h3/span/a')
        
        for name, url in zip(names,urls):
            yield {
                'name': name.get(),
                'url': url.attrib["href"]
            }

# Name of the file where the results will be saved
filename = "page1_japonais-paris.json"

# If file already exists, delete it before crawling (because Scrapy will concatenate the last and new results otherwise)
if filename in os.listdir('exo/'):
        os.remove('exo/' + filename)

# Declare a new CrawlerProcess with some settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/110.0.5481.78',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {'exo/' + filename: {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process.crawl(YelpSpider)
process.start()