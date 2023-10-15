import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim

import folium
# Read GTFS data
stops_df = pd.read_csv('gtfs/stops.txt')
routes_df = pd.read_csv('gtfs/routes.txt')
trips_df = pd.read_csv('gtfs/trips.txt', low_memory=False)
stop_times_df = pd.read_csv('gtfs/stop_times.txt',low_memory=False)



geolocator = Nominatim(user_agent="gtfs_map_app")

def get_coordinates(address):
    location = geolocator.geocode(address)
    return location.latitude, location.longitude

stops_df['latlon'] = stops_df['stop_name'].apply(get_coordinates)



# Convert lat/lon to Point geometries
gdf_stops = gpd.GeoDataFrame(stops_df, geometry=gpd.points_from_xy(stops_df['stop_lon'], stops_df['stop_lat']))

# If you have route shapes data in shapes.txt, read and create a GeoDataFrame for route shapes as well.
shapes_df = pd.read_csv('shapes.txt')
gdf_shapes = gpd.GeoDataFrame(shapes_df, geometry=gpd.points_from_xy(shapes_df['shape_pt_lon'], shapes_df['shape_pt_lat']))

# Create a map
m = folium.Map(location=[initial_lat, initial_lon], zoom_start=12)

# Add stops as markers
for idx, row in gdf_stops.iterrows():
    folium.Marker(location=[row['geometry'].y, row['geometry'].x], popup=row['stop_name']).add_to(m)

# Add route shapes as a polyline
folium.PolyLine(locations=gdf_shapes['geometry']).add_to(m)

# Save the map to an HTML file
m.save('gtfs_map.html')
'''
import pandas as pd
import folium



# Load your GTFS data
stops_df = pd.read_csv('gtfs_data/stops.txt')
routes_df = pd.read_csv('gtfs_data/routes.txt')
trips_df = pd.read_csv('gtfs_data/trips.txt', low_memory=False)
stop_times_df = pd.read_csv('gtfs_data/stop_times.txt', low_memory=False)

t = 0
i = 0
i_ = 0
t_ = 0
for x in stops_df['stop_lon']:
    t += 1
    i += x

for y in stops_df['stop_lat']:
    t_ += 1
    i_ += y

longitude = i / t
latitude = i_ / t_

m = folium.Map(location=[latitude, longitude], zoom_start=13)

# Add the polyline if there are valid coordinates
# Add markers for stops
for route_id in routes_df['route_id']:
    # Filter trips for the current route
    route_trips = trips_df[trips_df['route_id'] == route_id]
    for index, trip in route_trips.iterrows():
        # Get the sequence of stops for this trip
        stops_for_trip = stop_times_df[stop_times_df['trip_id'] == trip['trip_id']]
        coordinates = []
        for stop_id in stops_for_trip['stop_id']:
            if stop_id in stops_df['stop_id'].values:
                lat = stops_df.loc[stops_df['stop_id'] == stop_id, 'stop_lat'].values[0]
                lon = stops_df.loc[stops_df['stop_id'] == stop_id, 'stop_lon'].values[0]
                coordinates.append((lat, lon))
            else:
                # Handle missing 'stop_id' values (e.g., by skipping or logging)
                pass
        if coordinates:
            folium.PolyLine(locations=coordinates, color='blue', weight=2.5, opacity=1).add_to(m)

m.save('gtfs_map.html')
'''