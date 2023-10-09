from gtfs_functions import Feed, map_gdf
import geopandas as gpd
gtfs_path = 'your_gtfs_path'
feed = Feed(gtfs_path, time_windows=[0, 6 , 9, 15, 19, 22, 24])
seg_freq = feed.segments_freq

condition_dir = lines_freq.dir_id == 'Inbound'
condition_window = lines_freq.window == '6:00-9:00'

gdf = lines_freq.loc[(condition_dir & condition_window),:].reset_index()

gtfs.map_gdf(gdf= gdf,
	variable = 'ntrips',
	colors = ["#d13870","#e895b3","#55d992","#3ab071","#0e8955","#066a40"],
	tooltrip_var = ['route_name'],
	tooltip_labels=['Route: '],
	breaks = [5,10,20,50])

stops_freq.to_file('stops_freq.geojson', driver='GeoJSON')