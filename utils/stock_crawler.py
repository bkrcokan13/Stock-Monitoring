from bs4 import *
from logger import Logger
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
        self.stockName = None

        self.logger = Logger()

        
    def downloadStocksPage(self, stockname):

        if stockname is not None: 
            downloadPage = requests.get(
                f"{self.targetUrl}/{stockname}-hisse/", 
                headers=self.deviceHeader
            )

            if downloadPage.status_code == 200:
                 self.stockRawData = downloadPage.content
                 self.logger.successLogger("Stock page downloaded..!")

                 self.stockName = stockname

                 self.parseStocks()
            else: 
                self.logger.errorLogger(f"Stock page is not downloaded !...({downloadPage.status_code}) ")

        
    def parseStocks(self): 
        soup = BeautifulSoup(self.stockRawData, 'html.parser')


        # Get stock price and clear string
        getStockPrice = soup.find('p', attrs= {
            'class':'val'
        }).text.replace('₺','').replace(',','.')

 
        print(f"Stock : ({self.stockName.upper()}) - {getStockPrice}")
        
            

    def extractJsonFile(self):
        pass


app = StockCrawler()
app.downloadStocksPage(stockname="asels")