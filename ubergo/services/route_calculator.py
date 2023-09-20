import openrouteservice
from openrouteservice import convert
import folium
from geopy.geocoders import Nominatim

#initialize geolocator
geolocator = Nominatim(user_agent="aa")

#initialize the OpenRouteService client with your API key
client = openrouteservice.Client(key='API Key')

def route_calculator(ln1, lg1, ln2, lg2,km_cost,depart_cost, emission):

    coords = ((ln1,lg1),(ln2,lg2))
    res = client.directions(coords)
    geometry = client.directions(coords)['routes'][0]['geometry']
    decoded = convert.decode_polyline(geometry)

    distance=round(res['routes'][0]['summary']['distance']/1000)
    duration=round(res['routes'][0]['summary']['duration']/60)
    cost = round(distance*km_cost+depart_cost, 1)
    co2_emission = round(distance*emission,1)
    
    distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(distance)+" Km </strong>" +"</h4></b>"
    duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(duration)+" Mins. </strong>" +"</h4></b>"
    cost_txt = "<h4> <b>Cost :&nbsp" + "<strong>"+str(cost)+" $ </strong>" +"</h4></b>"
    co2_emission_txt = "<h4> <b>CO2 Emission :&nbsp" + "<strong>"+str(co2_emission)+" grams. </strong>" +"</h4></b>"

    #creates a map centered around the passenger's location
    m = folium.Map(location=[lg1,ln1],zoom_start=25, control_scale=True,tiles="cartodbpositron")

    #plot the route from the passenger's location to the desination location
    folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt+cost_txt+co2_emission_txt,max_width=300)).add_to(m)

    #marks the passenger's location
    folium.Marker(
        location=list(coords[0][::-1]),
        popup="Departure Location",
        icon=folium.Icon(color="green"),
    ).add_to(m)

    #marks the destination location
    folium.Marker(
        location=list(coords[1][::-1]),
        popup="Destination Location",
        icon=folium.Icon(color="red"),
    ).add_to(m)

    #saves the map to an HTML file
    m.save('map.html')

    y=[distance, duration, cost, co2_emission]
    return y

def driver_calculator(passenger_ln, passenger_lg, driver_ln, km_cost, depart_cost, driver_lg, emission):
    coords = ((passenger_ln,passenger_lg),(driver_ln, driver_lg))
    res = client.directions(coords)
    geometry = client.directions(coords)['routes'][0]['geometry']
    decoded = convert.decode_polyline(geometry)


    distance=round(res['routes'][0]['summary']['distance']/1000)
    duration=round(res['routes'][0]['summary']['duration']/60)
    co2_emission = round(distance*emission,1)
    cost = round(distance*km_cost+depart_cost, 1)

    distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(distance)+" Km </strong>" +"</h4></b>"
    duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(duration)+" Mins </strong>" +"</h4></b>"
    cost_txt = "<h4> <b>Cost :&nbsp" + "<strong>"+str(cost)+" $ </strong>" +"</h4></b>"
    co2_emission_txt = "<h4> <b>CO2 Emission :&nbsp" + "<strong>"+str(co2_emission)+" Grams </strong>" +"</h4></b>"

    #creates a map centered around the driver's location
    m = folium.Map(location=[driver_lg, driver_ln], zoom_start=15, control_scale=True, tiles="cartodbpositron")

    #plot the route from the driver's location to the passenger's location
    folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt+cost_txt+co2_emission_txt,max_width=300)).add_to(m)

    #marks the driver's location
    folium.Marker(
        location=list(coords[0][::-1]),
        popup="Driver's Location",
        icon=folium.Icon(color="green"),
    ).add_to(m)

    #marks the destination location
    folium.Marker(
        location=list(coords[1][::-1]),
        popup="Passenger's Location",
        icon=folium.Icon(color="red"),
    ).add_to(m)


    #saves the map to an HTML file
    m.save('map.html')
