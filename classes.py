##################### ÜBUNGSBLATT 1 #####################
import csv
import urllib.request
import time 
import matplotlib.pyplot as plt # loaded in virtual environment (venv) | activate with: source venv/bin/activate (MacOS/linux) or venv\Scripts\activate (Windows)
import json
import json

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
    def hashFunction(self, keyString):
        # TODO: Check if this hashfunction is OK
        hashValue = 0
        primeNumber = 79
        for char in keyString:
            # ord() transfers each char of the String to an int Unicode char
            hashValue = (hashValue * primeNumber + ord(char))
        return hashValue % self.size
    
    # Method to add stock to hashtable
    def addStock(self, stock):
        # Check if WKN already exists in hashtable
        index = 0;
        for i in self.table:
            if self.table[index] is not None and self.table[index].symbol == stock.symbol:
                print("Stock with Symbol " + stock.symbol + " already exists")
                return
            else:
                index += 1
                if index == self.size:
                    break
        # If Symbol does not already exist, add the new Stock to the hashtable
        # Index of new Stock gets calculated by setting the stocks Symbol as the keyValue for the hash function
        index = self.hashFunction(stock.symbol)
        # If the hashtable on the generated index is empty, add the stock to the index position of the hashtable
        if self.table[index] is None:
            self.table[index] = stock
        # Else a collision is detected
        # TODO: Review collision handling
        else:
            print("COLLISION DETECTED FOR KEY VALUE:", stock.symbol)
            print("Alternative hash value calculated")
            # First number of quadrating probing process declaration
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
    def deleteStock(self, symbol):
        foundStock = False
        # Index of Stock to delete gets calculated
        index = self.hashFunction(symbol)
        # If there is a stock at the index, set foundStock to true
        if self.table[index] is not None and self.table[index].symbol == symbol:
            foundStock = True
        # Else enter quadrating probing
        else:
            number = 1
            while True:
                probing_index = self.hashFunction(str(index + number**2))
                # If the values index & wkn are equal, set foundStock to true and set index to probing_index
                if self.table[probing_index] is not None and self.table[probing_index].symbol == symbol:
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
            print("Deleted the stock at index", index)
            print("Name:", self.table[index].name)
            print("WKN:", self.table[index].wkn)
            print("Symbol:", self.table[index].symbol)
            self.table[index] = None
        else:
            print("No Stock with Symbol", symbol, "found")

    # Method to import stock data from csv file
    def importStockData(self, symbol):
        import_folder = "import/"
        _csv = ".csv"
        file_path = import_folder + symbol + _csv
        index = self.hashFunction(symbol) # Calculate index of stock
        if not self.table[index] or self.table[index].symbol != symbol: # Check if stock with symbol exists
            print("No stock with Symbol", symbol, "found")
            return
        self.downloadStockData(symbol)
        if self.table[index] and self.table[index].symbol == symbol: # Check if stock with symbol exists
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                data_rows = list(reader)  # Read all rows into a list
                data_rows.pop(0)  # Remove header row
                reversed_data_rows = reversed(data_rows)  # Reverse the list of data rows

                # Iterate over the reversed data rows and add them to stock data
                count = 0
                for row in reversed_data_rows:
                    if count < 30:
                        self.table[index].data.append(row)
                        count += 1
                    else:
                        break

            print("Imported data for", symbol)
        else:
            print("No stock with WKN", symbol, "found")

    def downloadStockData(self, symbol):
    # Get current timestamp
        current_timestamp = int(time.time())
        # Calculate timestamp for 32 days ago
        period1_timestamp = current_timestamp - (30 * 24 * 60 * 60)  # 30 days in seconds
        # Construct the URL
        url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={period1_timestamp}&period2={current_timestamp}&interval=1d&events=history&includeAdjustedClose=true"
        # Send GET request to download data
        try:
            with urllib.request.urlopen(url) as response:
                print("Downloading data for", symbol)
                time.sleep(1)  # Wait for 1 second to avoid sending too many requests
                # Check if the request was successful
                if response.status == 200:
                    # Save data to a CSV file in the specified folder
                    import_folder = "import/"
                    csv_file_name = symbol + ".csv"
                    csv_file_path = import_folder + csv_file_name
                    with open(csv_file_path, 'wb') as csvfile:
                        csvfile.write(response.read())
                    print("Data saved under", csv_file_name, "in the folder", import_folder)
                else:
                    print("Failed to download data for", symbol)
        except urllib.error.URLError as e:
            print("Error:", e.reason)

    # Method to search for specific stock in the hashtable
    def searchStock(self, searchValue):
        # TODO: Review search function
        # Calculate index using hash function
        index = self.hashFunction(searchValue)
        
        # Check if the stock at the calculated index matches the search value
        if self.table[index] and (self.table[index].name == searchValue or self.table[index].symbol == searchValue):
            stock = self.table[index]
            self.printStockData(stock, index)
            return
        
        # If the stock is not found at the calculated index, perform linear search
        for i, stock in enumerate(self.table):
            if stock and (stock.name == searchValue or stock.symbol == searchValue):
                self.printStockData(stock, i)
                return
        
        # If the stock is not found, print a message
        print("No stock with name or symbol", searchValue, "found")

    # Method to print stock data
    def printStockData(self, stock, index):
        print("Name:", stock.name)
        print("WKN:", stock.wkn)
        print("Symbol:", stock.symbol)
        print("Index:", index)
        
        if stock.data:
            print("Last data entry:")
            print("Date:", stock.data[0][0])
            print("Open:", stock.data[0][1])
            print("High:", stock.data[0][2])
            print("Low:", stock.data[0][3])
            print("Close:", stock.data[0][4])
            print("Adj Close:", stock.data[0][5])
            print("Volume:", stock.data[0][6])
        else:
            print("No data found for this stock.")

    # Method to plot stock data
    def plotStockData(self, symbol):
        index = self.hashFunction(symbol)
        if self.table[index] and self.table[index].symbol == symbol:
            data = self.table[index].data
            reversed_data = data[::-1]  # Reverse the data
            dates = [row[0][5:] for row in reversed_data]
            close_prices = [float(row[4]) for row in reversed_data]

            plt.plot(dates, close_prices, marker='o', linestyle='-')
            plt.xlabel('Date')
            plt.ylabel('Close Price')
            plt.title(f'{self.table[index].name} Stock Close Prices Over the Last 30 Days')
            plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        else:
            print("No stock with Symbol", symbol, "found")

    # Method to save hashtable data to JSON
    def saveTable(self, fileName):
        data = []
        export_folder = "save/"
        file_path = export_folder + fileName + ".json"

        for index in range(self.size): # for loop to iterate over the hashtable
            if self.table[index] is not None:
                stock_data = {
                    "Index": index,
                    "Name": self.table[index].name,
                    "WKN": self.table[index].wkn,
                    "Symbol": self.table[index].symbol,
                    "Data": []
                }
                for row in self.table[index].data:
                    if len(row) == 7:  # Check if the row has 7 columns
                        stock_data["Data"].append({
                            "Date": row[0],
                            "Open": row[1],
                            "High": row[2],
                            "Low": row[3],
                            "Close": row[4],
                            "Adj Close": row[5],
                            "Volume": row[6]
                        })
                    else:
                        print("Invalid data format for stock with symbol", self.table[index].symbol)
                data.append(stock_data)

        with open(file_path, 'w') as file:
            json.dump(data, file)

        print("Hashtable data saved to", file_path)

    # Method to load hashtable data from JSON
    def loadTable(self, fileName):
            import_folder = "save/"
            file_path = import_folder + fileName + ".json"
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    for item in data: # for loop to iterate over the list of stocks
                        index = item["Index"]
                        name = item["Name"]
                        wkn = item["WKN"]
                        symbol = item["Symbol"]
                        stock = Stock(name, wkn, symbol)
                        for row in item["Data"]: # for loop to iterate over the list of stock data
                            stock.data.append([
                                row["Date"],
                                row["Open"],
                                row["High"],
                                row["Low"],
                                row["Close"],
                                row["Adj Close"],
                                row["Volume"]
                            ])
                        self.table[index] = stock
                    print("Hashtable data loaded from", file_path)
            except FileNotFoundError:
                print("The specified file was not found:", file_path)
            except json.JSONDecodeError:
                print("Error decoding the JSON file:", file_path)