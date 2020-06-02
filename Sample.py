import requests
import pandas as pd
import folium
import plotly.graph_objects as go
'''people = requests.get('https://252spynw7g.execute-api.ap-southeast-2.amazonaws.com/Prod/api/values/5')
data = pd.read_json(people.text)
print(data)
data_temp=data
temp=data_temp.groupby(['speeD_ZONE']).sum().reset_index(),
print(temp[0])'''
crash_data=pd.read_csv('Crashes_Last_Five_Years.csv')
crash_data['Year']="20"+crash_data['ACCIDENT_DATE'].str.split('/').str[-1]
crash_data= crash_data[crash_data['Year']=='2013']
print(crash_data['YOUNG_DRIVER'].sum())
'''map_data = crash_data.groupby(['LGA_NAME'])[['TOTAL_PERSONS']].sum().reset_index()
map_data = map_data.sort_values('TOTAL_PERSONS', ascending=False).head(1)

print(map_data['LGA_NAME'].values[0])'''


'''print(crash_data.columns)
print(crash_data.groupby(['ROAD_GEOMETRY'])[['TOTAL_PERSONS']].sum().reset_index())


temp=crash_data.groupby(['ROAD_GEOMETRY']).sum().reset_index()
print(temp[['ROAD_GEOMETRY','OLD_DRIVER','YOUNG_DRIVER']])'''

'''
crash_data['text'] = crash_data['LGA_NAME']
crash_data['Year']="20"+crash_data['ACCIDENT_DATE'].str.split('/').str[-1]
crash_data= crash_data[crash_data['Year']=='2013']
map_data2=crash_data.groupby(['LGA_NAME'])[['TOTAL_PERSONS']].sum().reset_index()
map_data1=crash_data.groupby(['LGA_NAME']).mean().reset_index()
map_data=pd.merge(map_data2, map_data1, left_on='LGA_NAME', right_on='LGA_NAME', how='inner')
print( (map_data['TOTAL_PERSONS_x']/sum(map_data['TOTAL_PERSONS_x'])*100))
map_data=map_data.sort_values('TOTAL_PERSONS_x', ascending=False).head(5)[['LGA_NAME','TOTAL_PERSONS_x']]

m = folium.Map([-37.8136, 144.9631], zoom_start=10)
m
for lat, lon, traffic, city in zip(map_data['LATITUDE'], map_data['LONGITUDE'], map_data['TOTAL_PERSONS_x'], map_data['LGA_NAME']):
    folium.CircleMarker(
        [lat, lon],
        radius=.01*2*traffic,
        popup = ('City:' + str(city).capitalize() + '<br>'
                'Total Number of Crashes:' + str(traffic)
                ),

        color='crimson',

        threshold_scale=[0,1,2,3],
        fill_color='crimson',
        fill=True,
        fill_opacity=0.7
        ).add_to(m)
m.save('map.html')

'''

