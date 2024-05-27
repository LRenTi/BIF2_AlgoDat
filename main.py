import sys
import argparse

class Station:
    def __init__(self, name):
        self.name = name
        self.connections = []

    def add_connection(self, connection):
        self.connections.append(connection)

class Connection:
    def __init__(self, line, to_station, cost):
        self.line = line
        self.to_station = to_station
        self.cost = cost

class Graph:
    def __init__(self):
        self.stations = {}

    def add_edge(self, line, from_station, to_station, cost):
        if from_station not in self.stations:
            self.stations[from_station] = Station(from_station)
        if to_station not in self.stations:
            self.stations[to_station] = Station(to_station)
        
        connection = Connection(line, self.stations[to_station], cost)
        self.stations[from_station].add_connection(connection)
        connection = Connection(line, self.stations[from_station], cost)
        self.stations[to_station].add_connection(connection)

    # TODO: Dijkstra implementation (Search for the shortest path)


# Nur zur Überprüfung - nicht Teil der Lösung
def print_graph(graph):
    for station_name, station in graph.stations.items():
        print(f"{station_name}:")
        for connection in station.connections:
            print(f"  -> {connection.to_station.name} (line: {connection.line}, cost: {connection.cost})")

def print_station(station):
    print(f"{station.name}:")
    for connection in station.connections:
        print(f"  -> {connection.to_station.name} (line: {connection.line}, cost: {connection.cost})")
    
def parse_graph(filename):
    graph = Graph()
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split(':')
            line_name = parts[0].strip()
            stations = parts[1].strip().split('"')[1::2]
            times = list(map(int, filter(None, parts[1].strip().split('"')[2::2])))  # Filter out empty strings
            if len(stations) != len(times) + 1:
                print("Invalid input format.")
                return None
            
            for i in range(len(stations) - 1):
                graph.add_edge(line_name, stations[i], stations[i+1], times[i])
    
    return graph

def main():
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("filename_graph", help="Input filename of the Network")
    parser.add_argument("-pp", "--pretty_print", action="store_true", help="Pretty print the Edges of the Network")
    parser.add_argument("start", nargs='?', help="Input the name of the start station")
    parser.add_argument("end", nargs='?', help="Input the name of the destination station")
    args = parser.parse_args()
    
    filename = args.filename_graph
    start = args.start
    end = args.end
    
    graph = parse_graph(filename)
    
    # TODO: Search for the shortest path
    
    if args.pretty_print and graph is not None:
        if start is not None:
            for station_name, station in graph.stations.items():
                if station_name == start:
                    selStation = station
                    break
            print("---------- Station ----------")
            print_station(selStation)
            print("-----------------------------")
        else:
            print("---------- Network ----------")
            print_graph(graph)
            print("-----------------------------")
    
    # TODO: Output of the shortest path (Which stations to take, which lines to use, where to transfer, total cost)

if __name__ == "__main__":
    main()
