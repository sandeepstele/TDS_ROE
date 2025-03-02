# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "pandas",
#     "scipy",
# ]
# ///


import pandas as pd
import json
from scipy.stats import pearsonr

# Load the JSON file
file_path = "./q-calculate-correlation__.json"

with open(file_path, "r") as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

# Calculate Pearson correlation coefficient
correlation, _ = pearsonr(df["A"], df["B"])

# Round to 3 decimal places
print(correlation)


import heapq
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

def haversine(coord1, coord2):
    R = 6371  # Earth's radius in km
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])
    
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat / 2) * 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) * 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def load_data(cities_file, flights_file):
    cities_df = pd.read_excel(cities_file, sheet_name="city")
    flights_df = pd.read_excel(flights_file, sheet_name="flights")
    
    coords = {row['City']: (row['Latitude'], row['Longitude']) for _, row in cities_df.iterrows()}
    
    graph = {}
    for _, row in flights_df.iterrows():
        city_from, city_to = row['From'], row['To']
        if city_from not in graph:
            graph[city_from] = []
        if city_to not in graph:
            graph[city_to] = []
        graph[city_from].append(city_to)
        graph[city_to].append(city_from)
    
    return coords, graph

def dijkstra(graph, coords, start, end):
    pq = [(0, start, [start])]
    visited = set()
    
    while pq:
        cost, city, path = heapq.heappop(pq)
        
        if city in visited:
            continue
        visited.add(city)
        
        if city == end and len(path) == 13:
            return ",".join(path)
        
        for neighbor in graph[city]:
            if neighbor not in visited:
                dist = haversine(coords[city], coords[neighbor])
                heapq.heappush(pq, (cost + dist, neighbor, path + [neighbor]))
    
    return "No valid path found"

# Load data from Excel files
cities_file = "/content/roe1.xlsx"
flights_file = "/content/roe1.xlsx"
coords, graph = load_data(cities_file, flights_file)

# Find the shortest path
shortest_path = dijkstra(graph, coords, "Kinshasa", "Houston")
print(shortest_path)
