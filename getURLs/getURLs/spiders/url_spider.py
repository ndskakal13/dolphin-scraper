''' Written by Nicholas Skakal.
Designed for use with Scrapy, MySQL and MySQLConnectorPython, and accompanying
files. I recommend unzipping dolphinScraper.zip to your directory of choice,
then leaving all files in their respective locations.
To run this spider: in a command terminal, navigate to ~/dolphinScraper/getURLs
and execute "scrapy crawl getURLs" (without quotes).
NOTE: must be connected to Le Moyne College's internal network for MySQL
connection to be made. '''

import scrapy
#from scrapy.crawler import CrawlerProcess
import sys
import mysql.connector
from mysql.connector import Error
from ..dateConverter import dateConverter
from ..items import GeturlsItem

class getURLs(scrapy.Spider):
    name = "getURLs"

    ''' constructor method: defines URLs to start crawl from, retrieves tab
                            counts and most recent date from MySQL database. '''
    def __init__(self):
        # define URLs to start populateStartURLs
        self.base_urls = [
            'https://thedolphinlmc.com/category/news-features/',
            'https://thedolphinlmc.com/category/opinion/',
            'https://thedolphinlmc.com/category/arts-leisure/',
            'https://thedolphinlmc.com/category/sports/',
            'https://thedolphinlmc.com/category/columns/',
            'https://thedolphinlmc.com/category/just-for-fun/',
            'https://thedolphinlmc.com/category/cheers-jeers/'
        ]

        # database credentials
        self.DB_HOST = "cscmysql.lemoyne.edu"
        self.DB_NAME = "dolphapp2019"
        self.DB_USER = "dolphapp"
        self.DB_PSWD = "dolphapp"

        # connect to database
        self.DBconnection = self.createConnection()

        # get tab counts from PageCounts and most recent article date in Archive
        tabTuples = self.getTabs()
        self.tabs = self.tupleToDict(tabTuples)
        self.mostRecent = self.getMostRecentDate()

        # close database connection
        self.closeConnection(self.DBconnection)

    # "main" of a Scrapy project. Executes parse() for each URL to be scraped.
    def start_requests(self):
        start_urls = self.populateStartURLs()
        
        for url in start_urls:
            yield scrapy.Request(url = url, callback = self.parse)

    ''' Purpose: parse a url and scrape data
        Input: response - HTML code for webpage
        Output: none
        Assumptions: if mostRecent == None, there are no articles in Archive '''
    def parse(self, response):
        pg_urls = response.css('a.homeheadline::attr(href)').getall()
        article_dts = response.css('span.time-wrapper::text').getall()
        article_dts_conv = []
        DC = dateConverter()

        for a in article_dts:
            # convert each article date to YYYY/MM/DD format
            article_dts_conv.append(DC.convertDate(a))

        counter = 0
        articleURL = GeturlsItem()
        
        while counter < len(pg_urls):
            if self.mostRecent != None:
                # if current article is more recent than most recent in database
                if DC.compareDates(article_dts_conv[counter], self.mostRecent):
                    articleURL['URL'] = pg_urls[counter]
                    yield articleURL
                    counter += 1
                else:
                    break # no need to add repeat articles
            else:
                articleURL['URL'] = pg_urls[counter]
                yield articleURL
                counter += 1

    ''' Purpose: connect to MySQL database
        Input: none
        Output: conn - database connection
        Assumptions: none '''
    def createConnection(self):
        try:
            conn = mysql.connector.connect(host = self.DB_HOST,
                                           user = self.DB_USER,
                                           passwd = self.DB_PSWD,
                                           database = self.DB_NAME )
            if conn.is_connected():
                print("Connected to database successfully.")
        except Error as err:
            conn = None
            print("Error connecting to database:", err)
            print("Scraping operations will not be attempted.")

        return conn

    ''' Purpose: retrieve tab counts from database
        Input: none
        Output: array of tab counts, or empty array if connection cannot be
                established
        Assumptions: none '''
    def getTabs(self):
        if (self.DBconnection != None):
            try:
                query = "SELECT * FROM PageCounts"

                cur = self.DBconnection.cursor()
                cur.execute(query)

                tabs = cur.fetchall()

                query = "DELETE FROM PageCounts"
                cur.execute(query) # clear database when done to prevent duplicates
                
                return tabs
            except Error as err:
                print("Error retrieving tab counts:" , err)
        else:
            return []

    ''' Purpose: retrieve most recent article date from database
        Input: none
        Output: most recent article date
        Assumptions: none '''
    def getMostRecentDate(self):
        if (self.DBconnection != None):
            try:
                query = "SELECT DISTINCT Date_Published FROM Archive ORDER BY Date_Published ASC"

                cur = self.DBconnection.cursor()
                cur.execute(query)

                dates = cur.fetchall()
                
                if len(dates) == 0: # no dates found in archive
                    return None
                else:
                    return dates[0]
            except Error as err:
                print("Error retrieving most recent date:" , err)
                return None
        else:
            return None

    ''' Purpose: close connection to database
        Input: conn - database connection
        Output: none
        Assumptions: none '''
    def closeConnection(self, conn):
        if conn != None:
            conn.close()

    ''' Purpose: change a list of two-element tuples to a dictionary
                 (format: key = tuple[0], value = tuple[1])
        Input: tList - list of tuples
        Output: dic - dictionary filled with key-value pairs
        Assumptions: tList contains only two-element tuples '''
    def tupleToDict(self, tList):
        dic = {}

        for t in tList:
            dic[t[0]] = t[1]

        return dic

    ''' Purpose: add URLs to scrape to 
        Input: none
        Output: urlList - list of URLs to be scraped
        Assumptions: tabs and base_urls are properly set up '''
    def populateStartURLs(self):
        counter = 0
        urlList = []
    
        while counter < len(self.base_urls):
            toParse = self.base_urls[counter]
            tabNo = int(self.tabs.get(toParse))
            tabCounter = 1

            while tabCounter <= tabNo:
                # first page of section has no page number at end
                if counter != 1:
                    toParse = toParse + "page/" + str(tabCounter) + "/"

                urlList.append(toParse)
                tabCounter += 1
                toParse = self.base_urls[counter] # reset url

            counter += 1

        return urlList

''' The code below runs the spider automatically when the module is run in Python. I had
    difficulty accessing the items file when running through Python as opposed to the command
    line. Thus I returned to using the command line to run spiders. '''
''' process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'items.json'
})

process.crawl(urlSpider)
process.start() '''
