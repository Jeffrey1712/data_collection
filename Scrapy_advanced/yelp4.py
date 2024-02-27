import os
import json
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

class YelpSpider(scrapy.Spider):

    name = "yelp"

    def __init__(self,**kwargs):
        # Retrieve list of urls
        for key, value in kwargs.items():
            if key == "search":
                self.start_urls = value[0:20] # For test purpose
            else: 
                logging.info("Argument not taken into account")
                
    def parse(self, response):
            yield {
                'name': response.xpath('/html/body/yelp-react-root/div[1]/div[4]/div[1]/div[1]/div/div/div[1]/h1/text()').get(),
                'star': response.xpath('/html/body/yelp-react-root/div[1]/div[4]/div[1]/div[1]/div/div/div[2]/div[2]/span[1]/text()').get(),
                'number_review': response.xpath('/html/body/yelp-react-root/div[1]/div[4]/div[1]/div[1]/div/div/div[2]/div[2]/span[2]/a/text()').get(),
                'address': response.xpath('/html/body/yelp-react-root/div[1]/div[6]/div/div[1]/div[2]/aside/section[1]/div/div[3]/div/div[1]/p[2]/text()').get(),
                'phone': response.xpath('/html/body/yelp-react-root/div[1]/div[6]/div/div[1]/div[2]/aside/section[1]/div/div[2]/div/div[1]/p[2]/text()').get(),
                'website': response.xpath('/html/body/yelp-react-root/div[1]/div[6]/div/div[1]/div[2]/aside/section[1]/div/div[1]/div/div[1]/p[2]/a/text()').get(),
            }


def define_user_input():
    search = input ("Que recherchez vous ? \n")
    localisation = input("Votre emplacement ?\n")
    return search,localisation


if __name__=="__main__": 
    # Retrieve url from a json file created previously
    file_path = "all_burger-lyon.json"
    with open(file_path) as file:
        json_content = json.load(file)
    list_urls = [
        "https://www.yelp.fr/" + element["url"]\
        for element in json_content
        ]
    # Name of the file where the results will be saved
    filename = "detail_search.json"
    # If file already exists, delete it before crawling (because Scrapy will concatenate the last and new results otherwise)
    if filename in os.listdir('exo/'):
            os.remove('exo/' + filename)
    # Declare a new CrawlerProcess with some settings
    process = CrawlerProcess(settings = {
        'USER_AGENT': 'Chrome/97.0',
        'LOG_LEVEL': logging.INFO,
        "FEEDS": {
            'exo/' + filename: {"format": "json"},
        }
    })
    # Start the crawling using the spider you defined above
    process.crawl(YelpSpider, search=list_urls)
    process.start()