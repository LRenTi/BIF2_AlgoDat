import sys
import argparse
import heapq
import time
#from collections import defaultdict

class Station:
    def __init__(self, name):
        self.name = name
        self.connections = []

    def add_connection(self, connection):
        self.connections.append(connection)

    def __lt__(self, other):
        return self.name < other.name

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

    def dijkstra(self, start, end):
        # Initialize the shortest distances and previous stations
        shortest_distances = {station: float('infinity') for station in self.stations.values()} # Initialize with infinity
        previous_stations = {station: None for station in self.stations.values()} # Initialize with None
        shortest_distances[self.stations[start]] = 0 # Start station has distance 0

        # Use a priority queue for the unvisited stations, with the distance as the priority
        unvisited_stations = [(0, self.stations[start])] # Start station has distance 0

        # Search for the shortest path
        while unvisited_stations: # O-Notation O(V) with V = number of stations
            # Use heapq to extract the station with the minimum distance
            current_distance, current_station = heapq.heappop(unvisited_stations) # O-Notation O(log V) with V = number of stations

            # Check if the destination station is reached
            if current_station == self.stations[end]: 
                # Reconstruct the path
                path = []
                line = None
                while previous_stations[current_station] is not None: # O-Notation O(V) with V = number of stations
                    for connection in previous_stations[current_station].connections: # O-Notation O(E) with E = number of connections
                        if connection.to_station == current_station:
                            line = connection.line
                            break
                    path.append((line, current_station.name))  # Line of the connection
                    current_station = previous_stations[current_station]  # Move to the previous station
                path.append((None, start))  # Start station has no line
                path.reverse()  # Reverse the path, O-Notation O(V) with V = number of stations
                return path, shortest_distances[self.stations[end]]  # Return the path and the total cost

            # Update the shortest distances and previous stations
            for connection in current_station.connections:
                distance = shortest_distances[current_station] + connection.cost
                if distance < shortest_distances[connection.to_station]:
                    shortest_distances[connection.to_station] = distance
                    previous_stations[connection.to_station] = current_station
                    # Add the updated station to the priority queue
                    heapq.heappush(unvisited_stations, (distance, connection.to_station))

        # If no path was found
        return None, float('infinity')


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

def print_shortest_path(path, distance, start, end):
    print("The shortest path from {} to {} is: \n".format(start, end), end="")
    prev_line = None
    for i, (line, station) in enumerate(path):
        if line is not None:
            if prev_line is not None and line != prev_line:
                print("[switch from {} to {}]".format(prev_line, line), end=" ")
            print("--> \n{}: {}".format(line, station), end=" ")
            if i == len(path) - 1:  # If this is the final station
                print("\n<<< You arrived at your destination {} >>>".format(station))
        else:
            print(station, end=" ")  # Start station has no line
        prev_line = line
    print("\nThe total cost/duration of this path is: {}".format(distance))

def main():
    # Argument parsing
    total_start_time = time.perf_counter()
    parser = argparse.ArgumentParser()
    parser.add_argument("filename_graph", help="Input filename of the Network")
    parser.add_argument("-pp", "--pretty_print", action="store_true", help="Pretty print the Edges of the Network")
    parser.add_argument("start", nargs='?', help="Input the name of the start station")
    parser.add_argument("end", nargs='?', help="Input the name of the destination station")
    args = parser.parse_args()
    
    filename = args.filename_graph
    start = args.start
    end = args.end
    
    parse_start_time = time.perf_counter()
    graph = parse_graph(filename)
    parse_end_time = time.perf_counter()
    
    if args.pretty_print and graph is not None:
        if start is not None and end is None:
            for station_name, station in graph.stations.items():
                if station_name == start:
                    selStation = station
                    break
                
            try:
                print("---------- Station ----------")
                print_station(selStation)
                print("-----------------------------")
            except:
                print("Station not found.")
    
    # Search for the shortest path
    if start is not None and end is not None:
        # Check if the start and end stations exist in the graph
        if start not in graph.stations or end not in graph.stations:
            print("Shortest Distance calculation not possible, one or more stations not found in textfile")
            return
        start_time = time.perf_counter()
        start_time = time.perf_counter()
        path, distance = graph.dijkstra(start, end)
        end_time = time.perf_counter()

        # Output of the shortest path (Which stations to take, which lines to use, where to transfer, total cost)
        print_shortest_path(path, distance, start, end)
        print()
        total_end_time = time.perf_counter()
        
        parse_elapsed_time = (parse_end_time - parse_start_time)*1000
        dj_elapsed_time = (end_time - start_time)*1000
        total_elapsed_time = (total_end_time - total_start_time)*1000
        print("Laufzeit des Parsen: {:.6f} ms".format(parse_elapsed_time))
        print("Laufzeit des Dijkstra-Algorithmus: {:.6f} ms".format(dj_elapsed_time))
        print("Gesamtlaufzeit: {:.6f} ms".format(total_elapsed_time))

if __name__ == "__main__":
    main()
