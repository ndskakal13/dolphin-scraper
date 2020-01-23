# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector
from mysql.connector import Error

class GetarticleinfoPipeline(object):
    def __init__(self):
        # database credentials
        self.DB_HOST = "cscmysql.lemoyne.edu"
        self.DB_NAME = "dolphapp2019"
        self.DB_USER = "dolphapp"
        self.DB_PSWD = "dolphapp"

        # attempt to connect to database
        try:
            self.DBconnection = mysql.connector.connect(host = self.DB_HOST,
                                                        user = self.DB_USER,
                                                        passwd = self.DB_PSWD,
                                                        database = self.DB_NAME)
            if self.DBconnection.is_connected():
                print("Connected to database successfully.")
        except Error as err:
            self.DBconnection = None
            print("Error connecting to database:", err)
            print("Scraped data will not be uploaded to database.")

    def process_item(self, item, spider):
        if (self.DBconnection != None):
            try:
                query = "INSERT INTO Archive (Title, Author, Date_Published, URL) VALUES (%s, %s, %s, %s)"
                recordTuple = (item['title'], item['author'], item['datePublished'], item['URL'])
                
                cur = self.DBconnection.cursor()
                cur.execute(query, recordTuple)
                self.DBconnection.commit()
                cur.close()
                print("Added", item, "to the database.")
            except Error as err:
                print("Failed to insert into MySQL table:", err)

        return item
