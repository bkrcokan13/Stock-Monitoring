import sqlite3, time, os 
from rich import table, console,box
from utils import monitor



class StmMonitor:

    def __init__(self):
        self.connDb = sqlite3.connect("stock-db.db")
        self.stock_name, self.stock_count = "", 0
        self.monitoring = monitor.Monitoring()

    
    
    

    # CRUD's operations
    def _getDbAllStocks(self):


        tableColumns = [
            "Stock ID", "Stock Name", "Stock Count"
        ]

        tableRows = []
        dataTable = table.Table(title="Stocks", box=box.HEAVY)

        tableConsole = console.Console()

        
        

        _sendCommandDd = self.connDb.execute(f"SELECT * FROM stock_table").fetchall()

        if _sendCommandDd == []:
            print("Database Is Empty !")
        else:
            for row in _sendCommandDd:

                dbList = list(row)
                

                # Temp, convert int to string (stock_id, stock_count) 
                dbList[0], dbList[2] = str(dbList[0]), str(dbList[2])


                # Add rich table rows
                tableRows.append(dbList)
            
            # Create table column 
            for column in tableColumns:
                dataTable.add_column(column)
            

            # Create table row
            for row in tableRows:
                dataTable.add_row(*row, end_section=True, style="bright_green") 

            # Print table
            tableConsole.print(dataTable)


    def _addNewStocks(self):
        try: 

            # Check empty data !
            if self.stock_name and self.stock_count is not None: 
                
               insertQuery = "INSERT INTO stock_table(stock_name, stock_count) VALUES(?,?)"
               
               # Define values
               stockValues = (self.stock_name, self.stock_count)

               # Execute SQL Insert Command
               self.connDb.execute(insertQuery, stockValues).connection.commit()

               print(f"New stock added..  ({self.stock_name} - {self.stock_count} )")
                    
            else: 
                print("Please enter stock name and count !")
        except sqlite3.OperationalError: 
            print(f"({self.stock_name}) is not added database...")
        except sqlite3.IntegrityError: 
            print(f"({self.stock_name}) is available in database...")

    def _deleteStocks(self):
        try:
            if self.stock_name is not None:
                
                deleteQuery = "DELETE FROM stock_table WHERE stock_name = ?"

                stockName = ([self.stock_name])
               

                # Execute SQL Command
                self.connDb.execute(deleteQuery, stockName).connection.commit()
                
            
                print(f"{self.stock_name} is removed from database...")

        except sqlite3.OperationalError: 
           print(f"{self.stock_name} is not removed from database...")
    
    def _deleteAllStocks(self):
        try:

            # Delete All Table Command
            deleteAllQuery = "DELETE FROM stock_table"

            # Clear Auto Increment 
            clearAutoIncQuery = "DELETE FROM sqlite_sequence WHERE name = 'stock_table'"
            
               
                

            # Execute SQL Command
            self.connDb.execute(deleteAllQuery).connection.commit()

            # Execute Auto Increment Command 
            self.connDb.execute(clearAutoIncQuery).connection.commit()
            
            print("All stocks deleted..") 

        except sqlite3.OperationalError:
            print("Stocks rows not deleting...")



    def _updateStocks(self): 
        try:
            if self.stock_name is not None:
                
                updateQuery = "UPDATE stock_table SET stock_count = ? WHERE stock_name = ?"
                updateStock = (self.stock_count, self.stock_name)

                # Execute SQL Command
                self.connDb.execute(updateQuery, updateStock).connection.commit()

                print(f"({self.stock_name}) is updated count ({self.stock_count})..")
                
        except sqlite3.OperationalError: 
            print(f"{self.stock_name} is not updated...")



    # Terminal UI
    def mainMenu(self):

        clearCmd = lambda : os.system('cls')

        while True: 
            
            clearCmd()
            # Table defines
            
            menuTable = table.Table(title="Stock Monitoring")
            menuConsole = console.Console()

            menuColumns = [
                "Code",
                "Title"
            ]   
            menuRows = [
                ["1", "Add Stock"],
                ["2", "Delete Stock"],
                ["3", "Update Stock"],
                ["4", "Show All Stocks"],
                ["5", "Delete All Stocks"],
                ["6", "Start Monitoring Stocks"]
            ]


            # Create Table Columns And Rows
            for column in menuColumns:
                menuTable.add_column(column, width=20, justify="center")   

            for row in menuRows:
                menuTable.add_row(*row, style="bright_green", end_section=True)
            

            # Print Table
            menuConsole.print(menuTable)

            userChoice = input("Command ->")

            if userChoice is not None:
 
                self.stock_name, self.stock_count = "", ""
                if userChoice == "1":

                    while True:
                            print(
                            """
                                |*************************|
                                |        ADD STOCK        |
                                |*************************|
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
                                |*************************|
                                |       DELETE STOCK      |
                                |*************************|
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
                                |*************************|
                                |       UPDATE STOCK      |
                                |*************************|
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
                                |*************************|
                                |       ALL STOCKS        |
                                |*************************|
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
                                    |*************************|
                                    |    DELETE ALL STOCKS    |
                                    |*************************|
                                """
                            )

                        self._deleteAllStocks()

                        input("...Press the any key and return the main menu...")
                        break
                elif userChoice == '6':
                    self.monitoring.startMonitor()
                                                        
            else:
                input("....Please enter any command....")    
                    
                    
app = StmMonitor()

app.mainMenu()
