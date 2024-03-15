##################### ÜBUNGSBLATT 1 #####################
import csv

class Stock:
    #Constructor
    def __init__(self, name, wkn, symbol):
        self.name = name
        self.wkn = wkn
        self.symbol = symbol
        # TODO: Add date and prices somehow (maybe price array?)
        self.data = []

class Hashtable:
    # Constructor
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    # Method to generate hash value from key value
    def hashFunction(self, keyValue):
        # TODO: Create our own hash function
        return hash(keyValue) % self.size
    
    # Method to add stock to hashtable
    def addStock(self, stock):
        # Index of new Stock gets calculated by setting the stocks WKN as the keyValue for the hash function
        index = self.hashFunction(stock.wkn)
        # If the hashtable on the generated index is empty, add the stock to the index position of the hashtable
        if self.table[index] is None:
            self.table[index] = stock
        # Else a collision is detected
        # TODO: Handle collision accordingly (Quadratische Soldierung)
        else:
            print("COLLISION DETECTED for KeyValue ", stock.wkn)

    # Method to delete stock from the hashtable
    def deleteStock(self, wkn):
        # Index of Stock to delete gets calculated
        index = self.hashFunction(wkn)
        # If there is a stock at the index, its set to None
        if self.table[index] is not None:
            print("Deleted the stock at index ", index)
            print("Name: ", self.table[index].name)
            print("WKN: ", self.table[index].wkn)
            print("Symbol: ", self.table[index].symbol)
            self.table[index] = None
        # Else print a warning
        else:
            print("No stock with WKN ", wkn, "found")

    # Method to import stock data from csv file
    # Not Working
    def importStockData(self, symbol, csv_file):
        import_folder = "import/"
        file_path = import_folder + csv_file
        index = self.hashFunction(symbol)  # Berechnen Sie den Index direkt mit der Hashfunktion basierend auf dem Symbol
        if self.table[index] and self.table[index].symbol == symbol:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Überspringen des Headers
                count = 0
                for row in reader:
                    if count < 30:
                        self.table[index].data.append(row)
                        count += 1
                    else:
                        break
            print("Imported data for ", symbol)
        else:
            print("No stock with symbol ", symbol, " found")
    
    def searchStock(self, searchValue):
        # Check if stock matches the search value
        for index, stock in enumerate(self.table):
            if stock is not None and (stock.name == searchValue or stock.symbol == searchValue):
                print("Name: ", stock.name)
                print("WKN: ", stock.wkn)
                print("Symbol: ", stock.symbol)
                print("Index: ", index)
                if stock.data:
                    print(stock.data)
                else:
                    print("No data found for this stock.")
                break
        else:
            print("No stock found with the given search value.")
        