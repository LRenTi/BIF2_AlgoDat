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
        # Stores shortest distance from start to each station, initialized with infinity for all stations
        shortest_distances = {station: float('infinity') for station in self.stations.values()}

        # Stores the previous station for each station in the shortest path from the start station, initialized with None for all stations, as none have been visited yet
        previous_stations = {station: None for station in self.stations.values()} 

        # Distance to the start station is initialized as 0
        shortest_distances[self.stations[start]] = 0

        # Priority queue (min-heap) to store the unvisited stations with the shortest distance from the start station
        # Each element is a tuple of distance and station (0 and start station for the start station)
        unvisited_stations = [(0, self.stations[start])]

        # Search for the shortest path
        while unvisited_stations:
            # Remove and return the station with the shortest distance from the priority queue
            # Always at first position of the heap (min-heap)
            # Ensures that the station with the shortest distance is visited next
            current_distance, current_station = heapq.heappop(unvisited_stations)

            # Check if the destination station is reached
            if current_station == self.stations[end]: 
                # Reconstruct the path
                path = []
                line = None
                # Traverse through previous stations from end to start
                while previous_stations[current_station] is not None:
                    # Find the used line for the connection
                    for connection in previous_stations[current_station].connections:
                        if connection.to_station == current_station:
                            line = connection.line
                            break
                    # Add the currenct line and station to the path
                    path.append((line, current_station.name))
                    # Move to the previous station
                    current_station = previous_stations[current_station]
                path.append((None, start))  # Add the start station to the path (without line)
                path.reverse()  # Reverse the path to start from the start station
                return path, shortest_distances[self.stations[end]]  # Return the path and the total cost

            # For each connection of the current station, update the shortest distance to the connected station
            for connection in current_station.connections:
                # Calculate the distance to the connected station
                distance = shortest_distances[current_station] + connection.cost
                # Check if the new distance is shorter than the previously stored distance to the connected station
                if distance < shortest_distances[connection.to_station]:
                    # Update the shortest distance to the connected station
                    shortest_distances[connection.to_station] = distance
                    # Update the previous station for the connected station
                    previous_stations[connection.to_station] = current_station
                    # Add the updated station to the priority queue
                    # Pushes multiple elements to the heap
                    # Final element is the station with the shortest distance
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
