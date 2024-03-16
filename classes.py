##################### ÜBUNGSBLATT 1 #####################
import csv
import urllib.request
import time 
import matplotlib.pyplot as plt # loaded in virtual environment (venv) | activate with: source venv/bin/activate (MacOS/linux) or venv\Scripts\activate (Windows)


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
            if self.table[index] is not None and self.table[index].wkn == stock.wkn:
                print("Stock with WKN " + stock.wkn + " already exists")
                return
            else:
                index += 1
                if index == self.size:
                    break
        # If WKN does not already exist, add the new Stock to the hashtable
        # Index of new Stock gets calculated by setting the stocks WKN as the keyValue for the hash function
        index = self.hashFunction(stock.wkn)
        # If the hashtable on the generated index is empty, add the stock to the index position of the hashtable
        if self.table[index] is None:
            self.table[index] = stock
        # Else a collision is detected
        # TODO: Review collision handling
        else:
            print("COLLISION DETECTED FOR KEY VALUE:", stock.wkn)
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
    def deleteStock(self, wkn):
        foundStock = False
        # Index of Stock to delete gets calculated
        index = self.hashFunction(wkn)
        # If there is a stock at the index, set foundStock to true
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
            print("Deleted the stock at index", index)
            print("Name:", self.table[index].name)
            print("WKN:", self.table[index].wkn)
            print("Symbol:", self.table[index].symbol)
            self.table[index] = None
        else:
            print("No Stock with WKN", wkn, "found")

    # Method to import stock data from csv file
    def importStockData(self, symbol):
        self.downloadStockData(symbol)
        import_folder = "import/"
        _csv = ".csv"
        file_path = import_folder + symbol + _csv
        index = None
        for i in range(self.size):
            if self.table[i] and self.table[i].symbol == symbol:
                index = i
                break
        if index is None:
            print("No stock with symbol", symbol, "found")
            return
        if self.table[index] and self.table[index].symbol == symbol: # Check if stock with wkn exists
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
        # TODO: Improve search function if possible
        index = 0
        for i in self.table:
            if self.table[index] is not None and self.table[index].name == searchValue or self.table[index] is not None and self.table[index].symbol == searchValue:
                print("Name: ", self.table[index].name)
                print("WKN: ", self.table[index].wkn)
                print("Symbol: ", self.table[index].symbol)
                print("Index: ", index)
                
                if self.table[index].data:
                    print("Last data entry: ")
                    print("Date: ", self.table[index].data[0][0])
                    print("Open: ", self.table[index].data[0][1])
                    print("High: ", self.table[index].data[0][2])
                    print("Low: ", self.table[index].data[0][3])
                    print("Close: ", self.table[index].data[0][4])
                    print("Adj Close: ", self.table[index].data[0][5])
                    print("Volume: ", self.table[index].data[0][6])
                else:
                    print("No data found for this stock.")
                break
            else:
                index += 1
            if(index == self.size):
                print("No stock with search-value", searchValue, "found")
    
    # Method to plot stock data
    def plotStockData(self, wkn):
        index = self.hashFunction(wkn)
        if self.table[index] and self.table[index].wkn == wkn:
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
            print("No stock with WKN", wkn, "found")


    # Method to save hashtable data to csv
    def saveTable(self, fileName):
        columnNames = ['Index','Name', 'WKN', 'Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        data = []
        export_folder = "save/"
        fileNameandPath = export_folder + fileName
        _csv = ".csv"

        for index in range(self.size):
            if self.table[index] is not None:
                stockData = [index, self.table[index].name, self.table[index].wkn, self.table[index].symbol]
                if self.table[index].data:
                    for row in self.table[index].data:
                        stockData.extend(row)
                data.append(stockData)  
        
        with open(fileNameandPath + _csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(columnNames)
            writer.writerows(data)

    def loadTable(self, fileName):
        import_folder = "save/"
        _csv = ".csv"
        file_path = import_folder + fileName + _csv
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                index = int(row[0])
                name = row[1]
                wkn = row[2]
                symbol = row[3]
                stock = Stock(name, wkn, symbol)
                stock.data = [row[4:]]
                self.table[index] = stock
        print("Table loaded from", fileName)