import sqlite3
import time
from colorama import *




class StmMonitor:

    def __init__(self):
        self.connDb = sqlite3.connect("stock-db.db")
        self.stock_name, self.stock_count = "", 0

    def _getDbAllStocks(self):

        _sendCommandDd = self.connDb.execute(f"SELECT * FROM stock_table").fetchall()

        if _sendCommandDd == []:
            print("Database Is Empty !")
        else:
             for row in _sendCommandDd:
                print(f"Stock ID : {row[0]}, \tStock Name: {row[1]}, \tStock Count: {row[2]}\n")

        # Close DB connection        
        self.connDb.close()
    

    def _addNewStocks(self):
        try: 

            # Check empty data !
            if self.stock_name and self.stock_count is not None: 
                
               insertQuery = "INSERT INTO stock_table(stock_name, stock_count) VALUES(?,?)"

               # Define values
               stockValues = (self.stock_name, self.stock_count)


               # Execute SQL Insert Command
               self.connDb.execute(insertQuery, stockValues).connection.commit()
               

               # Close DB Connection
               self.connDb.close()
               
            else: 
                print("Please enter stock name and count !")
        except sqlite3.OperationalError: 
           print("New stocks is not added !")
        except sqlite3.IntegrityError: 
            print(Fore.RED, f"Error: {self.stock_name} already exists in the database ! ")
            print(Style.RESET_ALL)

    def _deleteStocks(self):
        try:
            if self.stock_name is not None:
                
                deleteQuery = "DELETE FROM stock_table WHERE stock_name = ?"
                stockName = (self.stock_name)

                # Execute SQL Command
                self.connDb.execute(deleteQuery, stockName).connection.commit()
                

                # Close DB connection 
                self.connDb.close()

        except sqlite3.OperationalError: 
            print(Fore.RED, "Error : Stock is not delete !")

        


app = StmMonitor()

# Test funcs
app.stock_name = "TATEN"
app.stock_count = 15
app._addNewStocks()

app._getDbAllStocks()

    
 