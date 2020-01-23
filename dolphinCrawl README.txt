dolphinCrawl - A tool for getting article data from thedolphinlmc.com, the website of Le Moyne's student newspaper The Dolphin
developed by Nicholas Skakal '20

==================================================================================================================

PIP, SCRAPY, AND MYSQLCONNECTOR
===============================
To use these files, you must have the Python addons Scrapy and MySQLConnectorPython installed. You can do so with pip, a package installer developed for Python. (If you have Python 2 >=2.7.9 or Python 3 >=3.4 (downloaded from python.org), you likely already have pip installed.) In the case you don't, you can find instructions to install it at
https://pip.pypa.io/en/stable/installing/ .
Once you have pip installed, you can install the addons.

To install Scrapy, simply open a command terminal and enter the command:
pip install scrapy
and wait for it to complete.

To install MySQLConnectorPython, simply open a command terminal and enter the command:
pip install mysql-connector-python
and wait for it to complete.

CONNECTING TO THE MYSQL DATABASE
================================
In order to connect to the MySQL database, you must be on Le Moyne College's internal network. Data will not be uploaded to the database if executing these programs while not on the Le Moyne network. This can take place either on a desktop on campus at Le Moyne or by remote connection to a virtual Le Moyne desktop environment.

RUNNING THE FILES
=================
It is recommended that you not move, edit, or delete any files from their current locations. Simply unzip dolphinCrawl.zip to the directory of your choice.
Once this is done, open a command terminal and navigate to the directory you unzipped dolphinCrawl.zip to. Then go to dolphinCrawl/<spider>, where <spider> is the spider you want to run. Once there, run the following command in the command terminal:
scrapy crawl <spider-name>
where <spider-name> is the name given by "name" at the top of the spider.py file in its respective spiders folder.
The spiders are intended to be run in this order:
	- getPageCounts
	- getURLs
	- getArticleInfo
	- getPhotoInfo
You will have to navigate back up once in your directory once done to get to the next spider.