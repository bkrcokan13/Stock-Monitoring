from bs4 import *
import requests
import time 
import json


class StockCrawler: 
    def __init__(self):
        self.targetUrl = "https://www.getmidas.com/canli-borsa/"
        self.deviceHeader = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                           'AppleWebKit/537.36 (KHTML, like Gecko)'
                           'Chrome/116.0.0.0 Safari/537.36'),
            'Accept-Language': 'en-US, en;q=0.5'
        }

        self.stockRawData = None

    
    def _crawlerLogger(self):
        pass

    def downloadStocksPage(self):
        pass
    

    def parseStocks(self): 
        pass

    def extractJsonFile(self):
        pass
