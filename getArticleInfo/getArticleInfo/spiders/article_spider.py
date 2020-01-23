''' Written by Nicholas Skakal.
Designed for use with Scrapy, MySQL and MySQLConnectorPython, and accompanying
files. I recommend unzipping dolphinCrawl.zip to your directory of choice,
then leaving all files in their respective locations.
To run this spider: in a command terminal, navigate to
~/dolphinCrawl/getArticleInfo and execute "scrapy crawl getURLs" (without
quotes).
NOTE: must be connected to Le Moyne College's internal network for MySQL
connection to be made. '''

import scrapy
#from scrapy import CrawlerProcess
import sys
import mysql.connector
from mysql.connector import Error
from ..items import GetarticleinfoItem
from ..dateConverter import dateConverter

class getArticleInfo(scrapy.Spider):
    name = "getArticleInfo"

    ''' constructor method: defines URLs to start crawl from. '''
    def __init__(self):
        # database credentials
        self.DB_HOST = "cscmysql.lemoyne.edu"
        self.DB_NAME = "dolphapp2019"
        self.DB_USER = "dolphapp"
        self.DB_PSWD = "dolphapp"
        self.DBconnection = None

        # connect to database
        self.DBconnection = self.createConnection()

        # get URLs to scrape from
        self.URLs = self.getURLs()

        # close database connection
        self.closeConnection(self.DBconnection)

    # "main" of a Scrapy project. Executes parse() for each URL to be scraped.
    def start_requests(self):
        for url in self.URLs:
            yield scrapy.Request(url = url, callback = self.parse)

    ''' Purpose: parse a url and scrape data
        Input: response - HTML code for webpage
        Output: none
        Assumptions: none '''
    def parse(self, response):
        title = response.css('h1.storyheadline::text').get()
        author = response.css('a.creditline::text').get()
        # some articles have author tagged differently
        if author == None:
            #this contains author with their position (i.e., Staff Writer)
            authWithPos = response.css('span.storybyline::text').get()
            if authWithPos != None:
                commaIdx = authWithPos.rfind(",")
                author = titleWithPos[:commaIdx] #remove position from author
            else:
                author = None
        date = response.css('span.time-wrapper::text').get()

        DC = dateConverter()
        
        articleData = GetarticleinfoItem()
        articleData['title'] = title
        articleData['author'] = author
        articleData['datePublished'] = DC.convertDate(date)
        articleData['URL'] = response.request.url

        yield articleData

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
            print("Unable to get URLs to scrape. Scraping will not be attempted.")

        return conn
        
    ''' Purpose: get URLs to scrape from database
        Input: none
        Output: list of URLs to scrape
        Assumptions: none '''
    def getURLs(self):
        if (self.DBconnection != None):
            try:
                query = "SELECT * FROM URLs"

                cur = self.DBconnection.cursor()
                cur.execute(query)

                rows = cur.fetchall()
                urlStrs = []

                for r in rows:
                    urlStrs.append(r[0]) # URLs are uploaded as part of a tuple

                # database will be cleared after running getPhotoInfo
                #query = "DELETE FROM URLs"
                #cur.execute(query) # clear database when done to prevent duplicates
                
                return urlStrs
            except mysql.connector.Error as err:
                print("Failed to get URLs from MySQL database:", err)
                return []
        else:
            return []

    ''' Purpose: close connection to database
        Input: conn - database connection
        Output: none
        Assumptions: none '''
    def closeConnection(self, conn):
        if conn != None:
            conn.close()

''' The code below runs the spider automatically when the module is run in Python. I had
    difficulty accessing the items file when running through Python as opposed to the command
    line. Thus I returned to using the command line to run spiders. '''
''' process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'items.json'
})

process.crawl(articleSpider)
process.start() '''
