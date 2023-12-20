from bs4 import *
from logger import Logger
import json, time, requests, sqlite3, threading


class Monitoring: 
    def __init__(self):
        self.targetUrl = "https://www.getmidas.com/canli-borsa/"
        self.deviceHeader = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                           'AppleWebKit/537.36 (KHTML, like Gecko)'
                           'Chrome/116.0.0.0 Safari/537.36'),
            'Accept-Language': 'en-US, en;q=0.5'
        }

        self.connDb = sqlite3.connect("stock-db.db", check_same_thread=False)

        self.logger = Logger()

        self.dbStocks = []

        self.stocksRatings = []

        

        
    


    def startMonitor(self):
        self.logger.infoLogger("Monitoring started...")

        while True: 
            try:
                monitorTimer = threading.Timer(12, self.getStocks)
                monitorTimer.start()

                monitorTimer.join()

            except Exception as exp:
                print(exp)
                break

        
    def getDBStocks(self):

        try:
            # Call table 
            getStocksDb = self.connDb.execute("SELECT * FROM stock_table").fetchall()

            self.logger.infoLogger("Extracting DB Stocks...")
            # Check DB values 
            if getStocksDb == []:
                
                self.logger.errorLogger("Database is empty !")
                
                return False
            else: 
                
                self.dbStocks.clear()

                for stockdb in getStocksDb:
                    self.dbStocks.append(
                    {
                        'stock_name':stockdb[1],
                        'stock_count':stockdb[2]
                    }
                )
                    
                self.logger.successLogger("DB stocks extracted")
                    
                return True
        except Exception as errorCollect:
            self.logger.errorLogger(errorCollect)
                        


    def parseStocksRate(self):

        if(self.getDBStocks()):

            for stock in self.dbStocks:
                
                try:

                    # Download stock page 
                    downloadStockPage = requests.get(
                    self.targetUrl + f"{stock['stock_name']}-hisse",
                    self.deviceHeader
                    )


                    self.logger.infoLogger(f"Current Stock : {stock['stock_name']}")

                    # Shhhh sleept
                    time.sleep(1.1)

                    if (downloadStockPage.status_code == 200):
                        stockSoup = BeautifulSoup(downloadStockPage.content, 'html.parser')

                        self.logger.infoLogger("Stock price parsing....")


                        # Parse stock price
                        getStockPrice = stockSoup.find(
                            'p', attrs= {'class':'val'}
                        ).text.replace('₺','').replace(',','.')


                        # Calulcate stock pcs with stock price
                        stockPcsCalculate = (stock['stock_count'] * float(getStockPrice))


                        # Save temp stocks list
                        self.stocksRatings.append(
                            {
                                'stock_name': stock['stock_name'],
                                'stock_price': getStockPrice,
                                'stock_value': str(stockPcsCalculate)
                            }
                        )


                        self.logger.successLogger("Stock price parsed and value calculating is ok !")
                    else:
                        self.logger.errorLogger(f"Stock page not downloaded ! -- STATUS CODE : {downloadStockPage.status_code}")
                        break
                except Exception as parserError:
                    self.logger.errorLogger(parserError)
                finally:
                    break
            
            # Clear DB stocks list
            self.dbStocks.clear()


app = Monitoring()
app.startMonitor()