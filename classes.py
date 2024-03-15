##################### ÜBUNGSBLATT 1 #####################
class Stock:
    #Constructor
    def __init__(self, name, wkn, symbol):
        self.name = name
        self.wkn = wkn
        self.symbol = symbol
        # TODO: Add date and prices somehow (maybe price array?)

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

    # Method to search for specific stock in the hashtable
    def searchStock(self, searchValue):
        # TODO: Improve search function if possible
            # TODO: Add a warning if no stock is found
        index = 0
        for i in self.table:
            if self.table[index] is not None and self.table[index].name == searchValue or self.table[index] is not None and self.table[index].symbol == searchValue:
                print("Name: ", self.table[index].name)
                print("WKN: ", self.table[index].wkn)
                print("Symbol: ", self.table[index].symbol)
                print("Index: ", index)
                break
            else:
                index += 1
        