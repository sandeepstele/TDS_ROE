from haversine import haversine
import heapq

# Define coordinates for each city (latitude, longitude)
cities = {
    'Kinshasa': (-4.322447, 15.307045),
    'Brazzaville': (-4.263360, 15.242885),
    'Libreville': (0.416198, 9.467268),
    'Douala': (4.051066, 9.767430),
    'Yaoundé': (3.848000, 11.502100),
    'Lagos': (6.524379, 3.379206),
    'Accra': (5.603717, -0.186964),
    'Abidjan': (5.309660, -4.008256),
    'Dakar': (14.716677, -17.467686),
    'Bissau': (11.881700, -15.617000),
    'Conakry': (9.537950, -13.677290),
    'Bamako': (12.639232, -8.002889),
    'Nouakchott': (18.085400, -15.965000),
    'Rabat': (33.971589, -6.849813),
    'Casablanca': (33.573110, -7.589843),
    'Lisbon': (38.722252, -9.139337),
    'New York': (40.712776, -74.005974),
    'Houston': (29.760427, -95.369804)
}

# Define the flight network (direct connections between cities)
graph = {
    'Kinshasa': ['Brazzaville'],
    'Brazzaville': ['Kinshasa', 'Libreville'],
    'Libreville': ['Brazzaville', 'Douala'],
    'Douala': ['Libreville', 'Yaoundé'],
    'Yaoundé': ['Douala', 'Lagos'],
    'Lagos': ['Yaoundé', 'Accra'],
    'Accra': ['Lagos', 'Abidjan'],
    'Abidjan': ['Accra', 'Dakar'],
    'Dakar': ['Abidjan', 'Bissau'],
    'Bissau': ['Dakar', 'Conakry'],
    'Conakry': ['Bissau', 'Bamako'],
    'Bamako': ['Conakry', 'Nouakchott'],
    'Nouakchott': ['Bamako', 'Rabat'],
    'Rabat': ['Nouakchott', 'Casablanca'],
    'Casablanca': ['Rabat', 'Lisbon'],
    'Lisbon': ['Casablanca', 'New York'],
    'New York': ['Lisbon', 'Houston'],
    'Houston': ['New York']
}

def dijkstra(graph, cities, start, end):
    # Initialize distances and predecessor pointers
    distances = {city: float('inf') for city in cities}
    previous = {city: None for city in cities}
    distances[start] = 0
    queue = [(0, start)]
    
    while queue:
        current_distance, current_city = heapq.heappop(queue)
        
        # If we've reached the destination, break out
        if current_city == end:
            break
        
        if current_distance > distances[current_city]:
            continue
        
        for neighbor in graph.get(current_city, []):
            # Compute the Haversine distance between current city and neighbor
            leg_distance = haversine(cities[current_city], cities[neighbor])
            new_distance = current_distance + leg_distance
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_city
                heapq.heappush(queue, (new_distance, neighbor))
    
    # Reconstruct the shortest path from end to start
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path

start_city = 'Kinshasa'
end_city = 'Houston'
shortest_path = dijkstra(graph, cities, start_city, end_city)

# Print the route as a comma-separated list
print(", ".join(shortest_path))