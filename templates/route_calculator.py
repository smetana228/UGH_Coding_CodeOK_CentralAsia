import openrouteservice
from openrouteservice import convert
import folium
from geopy.geocoders import Nominatim
import os.path

geolocator = Nominatim(user_agent="aa")


def cost(taxi_type):
    if taxi_type == 'econom':
        depart_cost = 0.6
        km_cost=0.12
    if taxi_type == 'comfort':
        depart_cost = 0.8
        km_cost=0.14
    if taxi_type == 'business':
        depart_cost=1
        km_cost=0.16
    cost = [km_cost,depart_cost]
    return cost

def lnlg(depart, dest):
    location1 = geolocator.geocode(depart)
    ln1=location1.latitude
    lg1=location1.longitude
    location2=geolocator.geocode(dest)
    ln2=location2.latitude
    lg2=location2.longitude
    coords=((lg1,ln1),(lg2,ln2))
    print(location1.address,location2.address)
    return coords



#initialize the OpenRouteService client with your API key
client = openrouteservice.Client(key='5b3ce3597851110001cf6248959428a4c3da48e38933f1fd8fd5a38f')

def route_calculator(coords,km_cost,depart_cost, emission=192):
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
    m = folium.Map(location=coords[0][::-1],zoom_start=16, control_scale=True,tiles="cartodbpositron")
    driver_icon = folium.CustomIcon(
        icon_image='static/driver.png',
        icon_size=(40, 40),)
    #plot the route from the passenger's location to the desination location
    folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt+cost_txt+co2_emission_txt,max_width=300)).add_to(m)

    #marks the passenger's location
    folium.Marker(
        location=list(coords[0][::-1]),
        popup="Departure Location",
        icon=driver_icon,
    ).add_to(m)

    #marks the destination location
    folium.Marker(
        location=list(coords[1][::-1]),
        popup="Destination Location",
        icon=folium.Icon(color="red"),
    ).add_to(m)

    #saves the map to an HTML file
    m.save('passenger_map.html')

    y=[distance, duration, cost, co2_emission]
    return y

def driver_calculator(coords, emission=192):
    res = client.directions(coords)
    geometry = client.directions(coords)['routes'][0]['geometry']
    decoded = convert.decode_polyline(geometry)
    distance=round(res['routes'][0]['summary']['distance']/1000)
    duration=round(res['routes'][0]['summary']['duration']/60)
    co2_emission = round(distance*emission,1)

    driver_icon = folium.CustomIcon(
        icon_image='static/driver.png',
        icon_size=(40, 40),)

    passenger_icon = folium.CustomIcon(
        icon_image='static/passenger.png',
        icon_size=(20, 50),)

    distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(distance)+" Km </strong>" +"</h4></b>"
    duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(duration)+" Mins </strong>" +"</h4></b>"
    co2_emission_txt = "<h4> <b>CO2 Emission :&nbsp" + "<strong>"+str(co2_emission)+" Grams </strong>" +"</h4></b>"

    #creates a map centered around the driver's location
    m = folium.Map(location=coords[0][::-1], zoom_start=15, control_scale=True, tiles="cartodbpositron")

    #plot the route from the driver's location to the passenger's location
    folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt+co2_emission_txt,max_width=300)).add_to(m)

    #marks the driver's location
    folium.Marker(
        location=list(coords[0][::-1]),
        popup="Driver's Location",
        icon=driver_icon,
    ).add_to(m)

    #marks the destination location
    folium.Marker(
        location=list(coords[1][::-1]),
        popup="Passenger's Location",
        icon=passenger_icon,
    ).add_to(m)


    #saves the map to an HTML file
    m.save('driver_map.html')
    y=[distance, duration,co2_emission]
    return y

#t=lnlg('Absamat Masaliev','137A Toktonaliev')
#driver_calculator(t)
#y=cost('econom')
#d=lnlg('137A Toktonaliev', '182 Prospekt Mira Bishkek')
#route_calculator(d,y[0],y[1])