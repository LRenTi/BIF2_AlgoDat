##################### ÜBUNGSBLATT 1 #####################
import functions
import classes

def main():
    size = 1301 # Max 1000 Stocks + 30 % + 1 (for primary number)
    hashtable = classes.Hashtable(size)

    while True:
        functions.menuText()
        userInput = input("Input: ")

        if userInput == '1':
            # Add stock
            name = input("Enter stock name: ")
            wkn = input("Enter stock WKN: ")
            symbol = input("Enter stock symbol: ")
            stock = classes.Stock(name, wkn, symbol)
            # Add to hashtable
            hashtable.addStock(stock)

        elif userInput == '2':
            # Delete from hashtable
            deleteWKN = input("Enter WKN of stock to delete: ")
            hashtable.deleteStock(deleteWKN)

        elif userInput == '3':
            # TODO: Import from csv
            symbol = input("Input Symbol: ")
            csv_file = input("CSV file to import: ")
            hashtable.importStockData(symbol, csv_file)

        elif userInput == '4':
            # Search for Stock
            searchValue = input("Enter name or symbol of Stock: ")
            hashtable.searchStock(searchValue)

        elif userInput == '5':
            # TODO: Print plot
            print("Implement PLOT")

        elif userInput == '6':
            # TODO: Save hashtable to file
            print("Implement SAVE")

        elif userInput == '7':
            # TODO: Load hashtable from file
            print("Implement LOAD")

        elif userInput == '8':
            # Quit program
            break

        else:
            print("Invalid Input!")

if __name__ == "__main__":
    main()