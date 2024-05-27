import sys
import argparse
import heapq

# Usage python main.py (Noch umändern auf find_path filename_graph start ziel)

def read_graph(filename):
    graph = {}
    with open(filename, 'r') as file:
        for line in file:
            print(f"Reading line: {line.strip()}")  # Debug-Ausgabe
            parts = line.strip().split(':')
            if len(parts) != 2:
                continue
            line_name, stations_info = parts
            stations = stations_info.strip().split('" "')
            stations = [s.strip('"') for s in stations]
            for i in range(0, len(stations) - 2, 2):
                u = stations[i]
                v = stations[i + 2]
                weight = int(stations[i + 1])
                if u not in graph:
                    graph[u] = []
                if v not in graph:
                    graph[v] = []
                graph[u].append((v, weight))
                graph[v].append((u, weight))  # da der Graph ungerichtet ist
                print(f"Added edge from {u} to {v} with weight {weight}")  # Debug-Ausgabe
    return graph

# Nur zur Überprüfung - nicht Teil der Lösung
def print_graph(graph):
    for node in graph:
        print(f"{node}:")
        for neighbor, weight in graph[node]:
            print(f"  -> {neighbor} (cost: {weight})")
    print()

# TODO: Wenn read_graph bereits passt eigentlich nur mehr Dijkstra?

if __name__ == "__main__":
    
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("filename_graph", help="Input filename of the Network")
    # parser.add_argument("start", help="Input the name of the start station")
    # parser.add_argument("end", help="Input the name of the destination station")
    args = parser.parse_args()
    
    graph = read_graph(args.filename_graph)
    print_graph(graph)
