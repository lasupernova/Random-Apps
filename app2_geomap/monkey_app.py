#import libraries
import folium
import pandas as pd
import os
import cv2
from helpers import color_by_elevation, resize_pic, InfoFile

# create base layer Map-object to populate --> first layer
map = folium.Map(location=[50.779961, 6.109058], zoom_start=5, tiles="cartoDB positron") #pass [longitute, latitute] to "location"-argument

##add objects

# #add markers individually
# map.add_child(folium.Marker(location=[48.817066, 9.190845], popup="casita", icon=folium.Icon(color='pink')))

#better: add features (like markers) via feature groups --> this helps keeping things organized
#create feature group 
fg_pop = folium.FeatureGroup(name='Population Data')

#read JSON-file with data on country borders and population
pop_data=open('world.json','r', encoding='utf-8-sig').read()

#add Polygon layer (= first layer) - NOTE: Polygons are best to depict areas
fg_pop.add_child(folium.GeoJson(data=pop_data, style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 
10000000  <= x['properties']['POP2005'] < 20000000 else 'red'}))

# pichtml = '''<h3> This is the monkey-map</h3><br>
# <img src="monkey.jpg"><br>
# <p>foo bar</p>'''

pichtml = f'''<h3> This is the monkey-map!!!</h3><br>
                <img src="pics/monkeys.jpg" width="200" height="121"><br>
                <p>monkeys like us</p>'''

#add second fg
fg_monkey = folium.FeatureGroup(name='Monkey Spots')

#add objects (here: markers) to feature group --> first object in second layer (markers)
fg_monkey.add_child(folium.Marker(location=[48.817066, 9.190845], popup=pichtml, icon=folium.Icon(color='pink', icon='heart'))) #individually 


monkey_coords = [[37.786840, -122.412977],[48.678921, 9.044467],[48.755536, 9.145036],[51.327114, -116.180491],[12.501000, -70.029423],[40.703028, -73.996524],[34.134012, -118.321526],[29.968166, -90.078457], [36.020892, -121.549488], [40.746036, -73.844831]]
monkey_loc = ['Pineapple Hotel','Panzerkaserne', 'Buddha Lounge', 'Moraine Lake', 'Flamingo Island', 'Brooklyn Bridge Park', 'Hollywood Sign', 'Dooky Chase', 'Lucia...^.^','Unisphere']
for coordinates, loc_name in zip(monkey_coords, monkey_loc): #manually
    #get modified width and height
    height, width = resize_pic(loc_name, 'pics', maxsize=150)
    if loc_name == 'Panzerkaserne':
        #html-text to pass to popup-argument
        pichtml2 = f'''<h4> And this, my love, is how you take a GOOD picture...</h4><br>
                    <img src="pics/{loc_name}.jpg" width="{width}" height="{height}"><br>
                    <p>{loc_name}</p>'''
    else:

        #html-text to pass to popup-argument
        pichtml2 = f'''<img src="pics/{loc_name}.jpg" width="{width}" height="{height}"><br>
                <p>{loc_name}</p>'''
    # NOTE: Circlemarker()-radius is in pixel = remains same size while zooming, while Circle()-radius is in meters = becomes larger while zooming (!)
    fg_monkey.add_child(folium.CircleMarker(location=coordinates, popup=pichtml2, tooltip="Important Monkey Spot", color='red',radius=10, fill_color='red', fill_opacity=0.6))


#add third fg
fg_vol = folium.FeatureGroup(name='Random Volcanoes')

#load data into pandas
volcanoes = pd.read_csv('volcanoes.txt')

#iterate over df rows and add info to feature group automatically
for index, row in volcanoes.iterrows():
    #get relevant values
    lat = (row['LAT'])
    lon = (row['LON'])
    name = (row['NAME'])
    vol_type = (row['TYPE'])
    elev = (row['ELEV'])

    #html stylization to add to popup
    vol_html = f"""<h5>Volcano information:</h5>
    Name: {name}
    Type: {vol_type}
    Elevation: {elev}
    """

    #add child to fg based on info --> third layer
    fg_vol.add_child(folium.Marker(location=[lat,lon], popup=vol_html, icon=folium.Icon(color=color_by_elevation(elev), icon='exclamation-triangle', prefix='fa'))) #

#add feature group(s) to map
map.add_child(fg_pop)
map.add_child(fg_vol)
map.add_child(fg_monkey)

#add layerControl --> needs to be added AFTER feature groups that should be controlled
map.add_child(folium.LayerControl())

#save map
map.save('map.html')