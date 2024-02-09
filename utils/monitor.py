from bs4 import *
from rich import box, console
import  time  
import requests
import sqlite3
import threading
import rich.table as richTable
import os



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

        
        self.dbStocks = []
        self.stocksRatings = []
        self.dbCheck = False
        

        

        
    def startMonitor(self):

        print("Monitoring started...")
        self.getDBStocks()

        if self.dbCheck is True: 
             while True: 
                try:
                    monitorTimer = threading.Timer(5, self.parseStocksRate)
                    monitorTimer.start()

                    monitorTimer.join()

                except Exception as exp:
                    print(exp)
                    break


    # Add Initalize
    def getDBStocks(self):

        try:
            # Call table  
            getStocksDb = self.connDb.execute("SELECT * FROM stock_table").fetchall()

            print("Extracting DB Stocks...")
            # Check DB values 
            if getStocksDb == []:
                
                print("Database is empty !")
                
                self.dbCheck = False
            else: 
                # Clear Database Stocks List
                self.dbStocks.clear()
                
                print(getStocksDb)

                # Append DB Stocks List
                for stockdb in getStocksDb:
                    self.dbStocks.append(
                    {
                        'stock_name':stockdb[1],
                        'stock_count':stockdb[2]
                    }
                )
                    
                print("DB stocks extracted")
                    
                self.dbCheck = True
        except Exception as errorCollect:
            print(message=f"{errorCollect}")
                        
    def parseStocksRate(self):
        
        clearCmd = lambda : os.system('cls')
        for stock in self.dbStocks:
            try:
                # Download stock page 
                downloadStockPage = requests.get(
                    self.targetUrl + f"{stock['stock_name']}-hisse",
                    self.deviceHeader
                )

                # Info Current Stock
                print(f"Current Stock : {stock['stock_name']}")

                # Wait 1.1 Sec
                time.sleep(1.1)


                # HTML Status Code Check
                if (downloadStockPage.status_code == 200):

                    # Setup BS4
                    stockSoup = BeautifulSoup(downloadStockPage.content, 'html.parser')

                    print("Stock price parsing....")


                    # Parse stock price
                    getStockPrice = stockSoup.find(
                        'p', attrs= {'class':'val'}
                    ).text.replace('₺','').replace(',','.')


                    #! Only 2 last value
                    # Calulcate stock pcs with stock price
                    stockPcsCalculate = (stock['stock_count'] * float(getStockPrice))


                    # Save temp stocks list
                    self.stocksRatings.append(
                        {
                            'stock_name': stock['stock_name'],
                            'stock_price': getStockPrice,
                            'stock_value': str(stockPcsCalculate),
                            'stock_pcs' : stock['stock_count']
                        }
                    )


                    print("Stock price parsed and value calculating is ok !")
                else:
                    print(f"Stock page not downloaded ! -- STATUS CODE : {downloadStockPage.status_code}")
                    break
            except Exception as parserError:
                print(parserError)
                break

        stockTableColumn = [
            "Stock Name", "Stock Value", "Stock Value", "Stock PCS"
        ]

        stockTableRowData = []


        # Datatable Defines
        stockTableRich, stockTableConsole = richTable.Table(title="Stocks", box=box.ROUNDED),console.Console()

        for columnStocks in stockTableColumn:
            stockTableRich.add_column(
                columnStocks, 
                width=24,
                justify="center"
            )

        # Create Stock Rows
        for stockData in self.stocksRatings:
            stockTableRowData.append(
                [
                    f"{stockData['stock_name']}",
                    f"{stockData['stock_price']}",
                    f"{stockData['stock_value']}",
                    f"{stockData['stock_pcs']}"
                ]
            )

        # Create Rich Table
        
        for rowStocks in stockTableRowData:
            stockTableRich.add_row(
                *rowStocks,end_section=False
            )
        
        # Print Table
        stockTableConsole.print(stockTableRich, new_line_start=True)

        # Clear All
        stockTableRowData.clear()
        self.stocksRatings.clear()
        stockTableRowData.clear()
        

        time.sleep(3)
        clearCmd()
       

            
            
       
            
            