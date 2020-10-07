#import libraries
import folium
from folium import IFrame
import pandas as pd
import os
import cv2
from helpers import color_by_elevation, resize_pic, InfoFile

# create base layer Map-object to populate --> first layer
map = folium.Map(location=[50.779961, 6.109058], zoom_start=5, tiles="cartoDB positron") #pass [longitute, latitute] to "location"-argument

#create first feature group - containing Population data
fg_pop = folium.FeatureGroup(name='Population Data')

#read JSON-file with data on country borders and population
pop_data=open('world.json','r', encoding='utf-8-sig').read()

#add Polygon object - first object in first layer
fg_pop.add_child(folium.GeoJson(data=pop_data, style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 
10000000  <= x['properties']['POP2005'] < 20000000 else 'red'}))


#create second feature group - containing Markers regarding "Feminism"
fg_fem = folium.FeatureGroup(name='Feminism')

#add object (here: marker) to feature group --> first object in second layer
fg_fem.add_child(folium.Marker(location=[48.817066, 9.190845], popup='TEST', icon=folium.Icon(color='pink', icon='heart'))) #individually 

#add more objects to feature group --> second to n-th object in second layer
f_coords = [[48.875799, 2.361841], [-41.277751, 174.775920]]
f_event = ['Marie Sklodowska-Curie', 'Kate Sheppard']

#create InfoFile-object to get text-information regarding different events in f-event
info_df = InfoFile('media/texts.ods', 'odf')

for coordinates, f_name in zip(f_coords, f_event): #manually
    #get modified picture width and height
    height, width = resize_pic(f_name, 'media/pictures', maxsize=200)

    #get info text for event
    info_text = info_df.get_info(f_name)
    f_html = f'''<h4>{f_name}</h4><br>
                    <div><img src="media/pictures/{f_name}.jpg" width="{width}" height="{height}"></div><br>
                    <div>{info_text}</div>'''

    # NOTE: Circlemarker()-radius is in pixel = remains same size while zooming, while Circle()-radius is in meters = becomes larger while zooming (!)
    fg_fem.add_child(folium.CircleMarker(location=coordinates, popup=folium.Popup(f_html, width=700), tooltip="Feminist Milestone", color='red',radius=10, fill_color='red', fill_opacity=0.6))


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
map.add_child(fg_fem)

#add layerControl --> needs to be added AFTER feature groups that should be controlled
map.add_child(folium.LayerControl())

#save map
map.save('map.html')