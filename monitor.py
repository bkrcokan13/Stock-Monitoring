import sqlite3
import time




class StmMonitor:

    def __init__(self):
        self.connDb = sqlite3.connect("stock-db.db")
        self.stock_name, self.stock_count = "", 0

    def _getDbAllStocks(self):

        _sendCommandDd = self.connDb.execute(f"SELECT * FROM stock_table").fetchall()

        self.connDb.close()
        return _sendCommandDd
    

    def _addNewStocks(self):
        try: 
            if self.stock_name and self.stock_count is not None: 
               pass
            else: 
                print("Please enter stock name and count !")
        except sqlite3.OperationalError: 
           print("New stocks is not added !")

app = StmMonitor()

    
 