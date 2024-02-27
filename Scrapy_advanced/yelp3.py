import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

class YelpSpider(scrapy.Spider):

    name = "yelp"
    start_urls = ['https://www.yelp.fr/']

    def __init__(self,**kwargs):
        # Retrieve input arguments
        for key, value in kwargs.items():
            if key == "search":
                self.search = value
            elif key == "loc":
                self.loc = value
            else: 
                logging.info("INFO : Argument not taken into account")
                
    # Parse function for form request
    def parse(self, response):
        # FormRequest used to make a search in Paris
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'find_desc': self.search,
                'find_loc': self.loc
                },
            callback=self.after_search
        )

    # Callback used after login

    def after_search(self, response):
        
        names = response.xpath('//*[@id="main-content"]/div/ul/li/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div/h3/span/a/text()')
        urls = response.xpath('//*[@id="main-content"]/div/ul/li/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div/h3/span/a')
        
        for name, url in zip(names,urls):
            yield {
                'name': name.get(),
                'url': url.attrib["href"]
            }
            
            # Select the NEXT button and store it in next_page
        try:
            next_page = response.xpath('//*[@id="main-content"]/div/ul/li[13]/div/div[1]/div/div[11]/span/a').attrib["href"]

        except KeyError:          
            logging.info('No next page. Terminating crawling process.')
        
        else:
            yield response.follow(next_page, callback=self.after_search)

def define_user_input():
    search = input ("Que recherchez vous ? \n")
    localisation = input("Votre emplacement ?\n")
    return search,localisation


if __name__=="__main__": 
    # Retrieve user input
    search, loc = define_user_input()
    # Name of the file where the results will be saved
    filename = f"all_{search}-{loc}.json"
    # If file already exists, delete it before crawling (because Scrapy will concatenate the last and new results otherwise)
    if filename in os.listdir():
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
    process.crawl(YelpSpider, search=search, loc=loc)
    process.start()