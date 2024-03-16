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
            deleteSymbol = input("Enter Symbol of stock to delete: ")
            hashtable.deleteStock(deleteSymbol)

        elif userInput == '3':
            symbol = input("Enter stock symbol: ") # Symbol is needed to find the csv file
            hashtable.importStockData(symbol)

        elif userInput == '4':
            # Search for Stock
            searchValue = input("Enter name or symbol of Stock: ")
            hashtable.searchStock(searchValue)

        elif userInput == '5':
            # TODO: Print plot
            symbol = input("Enter Symbol of stock to plot: ")
            hashtable.plotStockData(symbol)

        elif userInput == '6':
            fileName = input("Enter filename: ")
            hashtable.saveTable(fileName)
            print("Data saved to /export")

        elif userInput == '7':
            fileName = input("Enter filename: ")
            hashtable.loadTable(fileName)
            print("Data loaded")

        elif userInput == '8':
            # Quit program
            break
        
        elif userInput == 'p':
            # Print hashtable
            print(hashtable.table)

        else:
            print("Invalid Input!")

if __name__ == "__main__":
    main()