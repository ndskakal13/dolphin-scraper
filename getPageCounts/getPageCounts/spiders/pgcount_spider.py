''' Written by Nicholas Skakal.
Designed for use with Scrapy, MySQL and MySQLConnectorPython, and accompanying
files. I recommend unzipping dolphinScraper.zip to your directory of choice,
then leaving all files in their respective locations.
To run this spider: in a command terminal, navigate to
~/dolphinScraper/getPageCounts and execute "scrapy crawl getURLs" (without
quotes).
NOTE: must be connected to Le Moyne College's internal network for MySQL
connection to be made. '''

import scrapy
#from scrapy.crawler import CrawlerProcess
import sys
from ..items import GetpagecountsItem

class getPageCounts(scrapy.Spider):
    name = "getPageCounts"
    start_urls = [
        'https://thedolphinlmc.com/category/news-features/',
        'https://thedolphinlmc.com/category/opinion/',
        'https://thedolphinlmc.com/category/arts-leisure/',
        'https://thedolphinlmc.com/category/sports/',
        'https://thedolphinlmc.com/category/columns/',
        'https://thedolphinlmc.com/category/just-for-fun/',
        'https://thedolphinlmc.com/category/cheers-jeers/'
    ]
    ''' Scrapy will automatically run the parse method for each URL in startURLs
        if start_requests() does not exist. '''

    ''' Purpose: parse a url and scrape data
        Input: response - HTML code for webpage
        Output: Scrapy Item object (similar to dictionary) containing URL scraped from and
                number of pages
        Assumptions: none '''
    def parse(self, response):
        count = GetpagecountsItem()

        tabCt = response.css('a.page::text').getall()
        
        count['URL'] = response.request.url
        count['tabCount'] = tabCt[len(tabCt) - 1] # only need the highest number

        yield count

''' The code below runs the spider automatically when the module is run in Python. I had
    difficulty accessing the items file when running through Python as opposed to the command
    line. Thus I returned to using the command line to run spiders. '''
''' process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'items.json'
})

process.crawl(pgCountSpider)
process.start() '''
