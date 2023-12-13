from colorama import *
from datetime import datetime



class Logger:

    def __init__(self):
        self.lastMessage = None    

        self.timeNowLogger = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


    def infoLogger(self, message):
        print(Fore.BLACK, Back.YELLOW, f"{self.timeNowLogger} - INFO : {message}")
        print(Fore.RESET, Back.RESET)
    
    def errorLogger(self, message):
        print(Fore.BLACK, Back.RED,f"{self.timeNowLogger} - ERROR : {message}")
        print(Fore.RESET, Back.RESET)


    def successLogger(self, message):
        print(Fore.BLACK,Back.GREEN,f"{self.timeNowLogger} - SUCCESS : {message}")
        print(Fore.RESET, Back.RESET, Back.RESET)
    
    def extractLogger(self):
        pass
