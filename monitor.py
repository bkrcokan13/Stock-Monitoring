import sqlite3
import time
from utils import logger




class StmMonitor:

    def __init__(self):
        self.connDb = sqlite3.connect("stock-db.db")
        self.stock_name, self.stock_count = "", 0


        self.eventLogger = logger.Logger()
    
    

    # CRUD's operations
    def _getDbAllStocks(self):

        _sendCommandDd = self.connDb.execute(f"SELECT * FROM stock_table").fetchall()

        if _sendCommandDd == []:
            self.eventLogger.infoLogger("Database Is Empty !")
        else:
             for row in _sendCommandDd:
                self.eventLogger.infoLogger(f"Stock ID : {row[0]}, \tStock Name: {row[1]}, \tStock Count: {row[2]}\n")
    

    def _addNewStocks(self):
        try: 

            # Check empty data !
            if self.stock_name and self.stock_count is not None: 
                
               insertQuery = "INSERT INTO stock_table(stock_name, stock_count) VALUES(?,?)"

               # Define values
               stockValues = (self.stock_name, self.stock_count)


               # Execute SQL Insert Command
               self.connDb.execute(insertQuery, stockValues).connection.commit()

               self.eventLogger.successLogger(f"New stock added..  ({self.stock_name} - {self.stock_count} )")
                    
            else: 
                self.eventLogger.errorLogger("Please enter stock name and count !")
        except sqlite3.OperationalError: 
            self.eventLogger.errorLogger(f"({self.stock_name}) is not added database...")
        except sqlite3.IntegrityError: 
            self.eventLogger.errorLogger(f"({self.stock_name}) is available in database...")

    def _deleteStocks(self):
        try:
            if self.stock_name is not None:
                
                deleteQuery = "DELETE FROM stock_table WHERE stock_name = ?"
                stockName = ([self.stock_name])

                # Execute SQL Command
                self.connDb.execute(deleteQuery, stockName).connection.commit()

                self.eventLogger.successLogger(f"{self.stock_name} is removed from database...")

        except sqlite3.OperationalError: 
            self.eventLogger.errorLogger(f"{self.stock_name} is not removed from database...")
    
    def _deleteAllStocks(self):
        try:

            # Delete All Table Command
            deleteAllQuery = "DELETE FROM stock_table"

            # Execute SQL Command
            self.connDb.execute(deleteAllQuery).connection.commit()
            
            self.eventLogger.successLogger("All stocks deleted..") 

        except sqlite3.OperationalError:
            self.eventLogger.errorLogger("Stocks rows not deleting...")



    def _updateStocks(self): 
        try:
            if self.stock_name is not None:
                
                updateQuery = "UPDATE stock_table SET stock_count = ? WHERE stock_name = ?"
                updateStock = (self.stock_count, self.stock_name)

                # Execute SQL Command
                self.connDb.execute(updateQuery, updateStock).connection.commit()

                self.eventLogger.successLogger(f"({self.stock_name}) is updated count ({self.stock_count})..")
                
        except sqlite3.OperationalError: 
            self.eventLogger.errorLogger(f"{self.stock_name} is not updated...")



    # Terminal UI
    def mainMenu(self):
        menuArt = """
                        |-------------------------|
                        |       STM V.1.0.0       |
                        |-------------------------|
                        |  1- (Add Stock)         |                             
                        |  2- (Delete Stock)      |                              
                        |  3- (Update Stock)      |                              
                        |  4- (Show All Stocks)   |                              
                        |  5- (Delete All Stocks) | 
                        |-------------------------|                                                                              
                                                                                    
                   
                    """
        while True: 
            print(menuArt)
            userChoice = input("->")

            if userChoice is not None:
 
                self.stock_name, self.stock_count = "", ""
                if userChoice == "1":

                    while True:
                            print(
                            """
                                |-------------------------|
                                |       STM V.1.0.0       |
                                |-------------------------|
                            """
                            )
                            stName, stCount = input("Stock Name : "), input("Stock Count : ")

                            if stName and stCount is not None:
                                

                                # Get user data
                                self.stock_name, self.stock_count = stName, stCount

                                # Call add new stock function
                                self._addNewStocks()

                                # Show updated database
                                self._getDbAllStocks()


                                input("...Press the any key and return the main menu ")


                                # Clear global variables
                                self.stock_name, self.stock_count = "", ""
                                break
                            else:
                                elseChoice = input("Please enter stock name and stock count.. (Return Menu : Q)")


                                # Return menu 
                                if elseChoice == "Q" or "q":
                                    break
                                else:
                                    continue
                
                elif userChoice == '2':
                    while True:
                        # Clear stock name and count
                        self.stock_name,self.stock_count = "", ""
                        print(
                            """
                                |-------------------------|
                                |       STM V.1.0.0       |
                                |-------------------------|
                            """
                        )

                        # Get User value
                        stName = input("Stock Name : ")

                        if stName is not None:
                            
                            # Update global name varialable
                            self.stock_name = stName


                            # Delete selected stocks
                            self._deleteStocks()

                            # Show updated database
                            self._getDbAllStocks()
                            input("...Press the any key and return the main menu ")


                            # Clear global varialable
                            self.stock_name, self.stock_count = "", ""
                            break
                elif userChoice == '3':
                    while True:
                        # Clear stock name and count
                        self.stock_name,self.stock_count = "", ""
                        print(
                            """
                                |-------------------------|
                                |       STM V.1.0.0       |
                                |-------------------------|
                            """
                        )

                        # Get User value
                        stName, stCount = input("Updated Stock Name: "), input("Updated Stock Count: ")

                        if stName is not None:
                            
                            # Update global name varialable
                            self.stock_name = stName


                            # Delete selected stocks
                            self._updateStocks()

                            # Show updated database
                            self._getDbAllStocks()
                            input("...Press the any key and return the main menu ")


                            # Clear global varialable
                            self.stock_name, self.stock_count = "", ""
                            break
                elif userChoice == '4':
                    while True:
                        self.stock_name, self.stock_count = "",""

                        print(
                            """
                                |-------------------------|
                                |       STM V.1.0.0       |
                                |-------------------------|
                            """
                        )

                        self._getDbAllStocks()

                        input("...Press the any key and return the main menu ...")
                        break

                elif userChoice == '5':

                    while True:
                        self.stock_name, self.stock_count = "",""

                        print(
                                """
                                    |-------------------------|
                                    |       STM V.1.0.0       |
                                    |-------------------------|
                                """
                            )

                        self._deleteAllStocks()

                        input("...Press the any key and return the main menu...")
                        break
                    

                                                    
            else:
                input("....Please enter any command....")    
                    
                    
app = StmMonitor()

app.mainMenu()