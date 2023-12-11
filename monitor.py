import sqlite3
import time




class StmMonitor:

    def __init__(self):
        self.connDb = sqlite3.connect("stock-db.db")

    def getDbAllStocks(self):

        _sendCommandDd = self.connDb.execute(f"SELECT * FROM stock_table").fetchall()

        self.connDb.close()
        return _sendCommandDd
    

    def addNewStocks(self, stockName, stockCount):
        if stockName and stockCount is not None: 
            if isinstance(stockCount, int): 
                print("OK")
            else:
                print("Stock count is not Integer !")
        else: 
            print("Please enter stock name and count !")



app = StmMonitor()



    

    
 