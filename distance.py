from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Initialize the Nominatim geocoder with a custom user agent.
geolocator = Nominatim(user_agent="geo_query_script")

def get_location(query):
    """Fetch coordinates of a location using geopy's Nominatim geocoder."""
    location = geolocator.geocode(query, exactly_one=True)
    if location:
        return location
    else:
        print(f"Error: No results found for {query}")
        return None

def get_distance(location_1, location_2):
    """Calculate distance between two locations given their coordinates."""
    # Use geopy's location object attributes for latitude and longitude
    coords1 = (location_1.latitude, location_1.longitude)
    coords2 = (location_2.latitude, location_2.longitude)
    return geodesic(coords1, coords2).kilometers

# Example usage
location_1 = get_location('Mumbai')
location_2 = get_location('Delhi')

if location_1 and location_2:
    distance = get_distance(location_1, location_2)
    print(f"Distance between Mumbai and Delhi: {distance:.2f} km")
else:
    print("One or both locations could not be found.")