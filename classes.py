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
    def hashFunction(self, keyString):
        # TODO: Check if this hashfunction is OK
        keyValue = 0
        for char in keyString:
            # ord() transfers each char of the String to an int Unicode char
            keyValue += ord(char)
        return keyValue % self.size
    
    # Method to add stock to hashtable
    def addStock(self, stock):
        # TODO If same WKN is entered twice, do NOT add
        # Index of new Stock gets calculated by setting the stocks WKN as the keyValue for the hash function
        index = self.hashFunction(stock.wkn)
        # If the hashtable on the generated index is empty, add the stock to the index position of the hashtable
        if self.table[index] is None:
            self.table[index] = stock
        # Else a collision is detected
        # TODO: Review collision handling
        else:
            print("COLLISION DETECTED FOR KEY VALUE: ", stock.wkn)
            print("Alternative hash value calculated")
            # First number of probing process declaration
            number = 1
            while True:
                probing_index = self.hashFunction(str(index + number**2))
                # If the hashtable at the new index is empty, place stock at new index and exit loop
                if self.table[probing_index] is None:
                    self.table[probing_index] = stock
                    break
                # Else add 1 to number
                else:
                    number += 1
                    if(number) >= self.size:
                        print("No possible index for this stock")

    # Method to delete stock from the hashtable
    def deleteStock(self, wkn):
        foundStock = False
        # Index of Stock to delete gets calculated
        index = self.hashFunction(wkn)
        # If there is a stock at the index, set foundStock to ture
        if self.table[index] is not None and self.table[index].wkn == wkn:
            foundStock = True
        # Else enter quadrating probing
        else:
            number = 1
            while True:
                probing_index = self.hashFunction(str(index + number**2))
                # If the values index & wkn are equal, set foundStock to true and set index to probing_index
                if self.table[probing_index] is not None and self.table[probing_index].wkn == wkn:
                    foundStock = True
                    index = probing_index
                    break
                # Else add 1 to number
                else:
                    number += 1
                    if(number) >= self.size:
                        break
        # If the stock is found, delete it
        if foundStock:
            print("Deleted the stock at index ", index)
            print("Name: ", self.table[index].name)
            print("WKN: ", self.table[index].wkn)
            print("Symbol: ", self.table[index].symbol)
            self.table[index] = None
        else:
            print("No Stock with WKN", wkn, "found")

    # Method to search for specific stock in the hashtable
    def searchStock(self, searchValue):
        # TODO: Improve search function if possible
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
            if(index == self.size):
                print("No stock with search-value", searchValue, "found")
        