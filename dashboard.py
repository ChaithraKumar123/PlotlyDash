
import dash
import requests
import pandas as pd
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
import folium
from dash.dependencies import Input, Output

people = requests.get('https://252spynw7g.execute-api.ap-southeast-2.amazonaws.com/Prod/api/values/5')
data = pd.read_json(people.text)
crash_data1=pd.read_csv('Crashes_Last_Five_Years.csv')
crash_data1['Year']="20"+crash_data1['ACCIDENT_DATE'].str.split('/').str[-1]
crash_data1['TOTAL_PERSONS_Injured']=crash_data1['TOTAL_PERSONS']
crash_data1['TOTAL_PERSONS']= 1
crash_data1=crash_data1[crash_data1['Year']!='2019']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.GRID])



app.layout = html.Div([
    html.H1("Crash Data Statistics in Victoria",style={
            'textAlign': 'center',
            'color': 'white'
        }),


dbc.Row([dbc.Col(html.P("Select Year",style={

            'color': 'white'
        }),md=1),dbc.Col( dcc.Dropdown
        (
            id='dropdown_year',
         options=[{'label': i, 'value': i} for i in crash_data1['Year'].unique()],
         value='2013'
        ))],align="end"),

    html.Br(),

    dbc.Row([dbc.Col([ html.Div(
        [html.Img(src="https://img.icons8.com/ios-filled/50/000000/place-marker.png"),
         html.P("Region with highest crashes"),
         html.P(id="RegionCrash")],
    style={"backgroundColor":"white"})],md=2), dbc.Col([],md=1),dbc.Col([ html.Div(
        [html.Img(src="https://img.icons8.com/ios-filled/50/000000/car-crash.png"),
         html.P("Road Geometry with highest crashes "),
         html.P(id="Geo_crash")],
    style={"backgroundColor":"white","width":"100"})],md=3),dbc.Col([],md=1),dbc.Col([ html.Div(
        [html.Img(src="https://img.icons8.com/ios-filled/50/000000/boy.png"),
         html.P("Number of Young drivers Injured"),
         html.P(id="Young_Driver")],
    style={"backgroundColor":"white","width":"100"})],md=2),dbc.Col([],md=1),dbc.Col([ html.Div(
        [html.Img(src="https://img.icons8.com/ios-filled/50/000000/elderly-person.png"),
         html.P("Number of Old drivers Injured"),
         html.P(id="Old_Driver")],
    style={"backgroundColor":"white","width":"100"})],md=2)]),

dbc.Container(

    [

        html.Br()
        ,
        dbc.Row([

        dbc.Col([
         html.P("Crashes based on Region in Victoria", id="p_Crashes",style={

            'color': '#1f77b4',
            'font-family':'Sherif',
             'font-size':20,
             'left-align':"20%"

        }),
         html.Iframe(id='map',width="100%",height="500")
            ],md=12),



            ],align="end")
    ]

,fluid=True),
html.Br(),
dbc.Container(dbc.Row(dbc.Col([dcc.Graph(id='dd-graph_pie')],md=12),align="end"),fluid=True),
html.Br(),
    dbc.Container([


        dbc.Row([
            dbc.Col(html.P("Select Road Geometry",style={

            'color': 'white'
        }),md=2),
            dbc.Col([

            dcc.Dropdown(
         id='dropdown1',
         options=[{'label': i, 'value': i} for i in data['roaD_GEOMETRY'].unique()],
         value='Cross intersection',
        placeholder="select "

     ),


           ])

    ,


 ],align="end")],fluid=True),
dbc.Container(
    dbc.Row(dbc.Col(dcc.Graph(id='dd-graph',config={'displayModeBar': False}),md=12),align="end"),fluid=True


),

html.Br(),
dbc.Container(
    dbc.Row(dbc.Col(dcc.Graph(id='dd-graph3'),md=12),align="end"),fluid=True


)]
    ,
style={'background-color':'#191919'}
)

@app.callback(
    Output(component_id='RegionCrash', component_property='children'),
    [Input(component_id='dropdown_year', component_property='value')])
def update_value(value):
    crash_data = crash_data1[crash_data1['Year'] == value]
    map_data = crash_data.groupby(['LGA_NAME'])[['TOTAL_PERSONS']].sum().reset_index()
    map_data=map_data.sort_values('TOTAL_PERSONS', ascending=False).head(1)
    return (map_data['LGA_NAME'].values[0] +" - "+str(map_data['TOTAL_PERSONS'].values[0]))

@app.callback(
    Output(component_id='Young_Driver', component_property='children'),
    [Input(component_id='dropdown_year', component_property='value')])
def update_value(value):
    crash_data = crash_data1[crash_data1['Year'] == value]
    return ("   "+str(crash_data['YOUNG_DRIVER'].sum()))

@app.callback(
    Output(component_id='Old_Driver', component_property='children'),
    [Input(component_id='dropdown_year', component_property='value')])
def update_value(value):
    crash_data = crash_data1[crash_data1['Year'] == value]

    return ("   "+str(crash_data['OLD_DRIVER'].sum()))

@app.callback(
    Output(component_id='Geo_crash', component_property='children'),
    [Input(component_id='dropdown_year', component_property='value')])
def update_value(value):
    crash_data = crash_data1[crash_data1['Year'] == value]
    map_data = crash_data.groupby(['ROAD_GEOMETRY'])[['TOTAL_PERSONS']].sum().reset_index()
    map_data=map_data.sort_values('TOTAL_PERSONS', ascending=False).head(1)
    return (map_data['ROAD_GEOMETRY'].values[0].upper() +" - "+str(map_data['TOTAL_PERSONS'].values[0]).upper())

@app.callback(
    Output(component_id='map', component_property='srcDoc'),
    [Input(component_id='dropdown_year', component_property='value')])
def update_value(value):
    crash_data = crash_data1[crash_data1['Year'] == value]
    map_data2 = crash_data.groupby(['LGA_NAME'])[['TOTAL_PERSONS']].sum().reset_index()
    map_data1 = crash_data.groupby(['LGA_NAME']).mean().reset_index()
    map_data = pd.merge(map_data2, map_data1, left_on='LGA_NAME', right_on='LGA_NAME', how='inner')
    m = folium.Map([-37.8136, 144.9631], zoom_start=10,tiles='Stamen Toner')

    for lat, lon, traffic, city in zip(map_data['LATITUDE'], map_data['LONGITUDE'], map_data['TOTAL_PERSONS_x'],
                                       map_data['LGA_NAME']):
        folium.CircleMarker(
            [lat, lon],
            radius=.01 * 2 * traffic,
            popup=('City:' + str(city).capitalize() + '<br>'
                                                      'Total Number of Crashes:' + str(traffic)
                   ),

            color='crimson',

            threshold_scale=[0, 1, 2, 3],
            fill_color='crimson',
            fill=True,
            fill_opacity=0.7
        ).add_to(m)
    m.save('map.html')
    return(open('map.html','r').read())

@app.callback(
    Output(component_id='dd-graph_pie', component_property='figure'),
    [Input(component_id='dropdown_year', component_property='value')])
def update_value(value):
    crash_data = crash_data1[crash_data1['Year'] == value]
    pie_chart= crash_data.groupby(['ROAD_GEOMETRY'])[['TOTAL_PERSONS']].sum().reset_index()

    trace1 = go.Figure(data=[go.Bar(x=pie_chart['ROAD_GEOMETRY'], y=pie_chart['TOTAL_PERSONS'],opacity=0.75,textposition='outside',
                    marker_color='rgb(158,202,225)', marker_line_color='rgb(255,255,255)',
                    marker_line_width=1.5,text=pie_chart['TOTAL_PERSONS'],texttemplate='%{text:.2s}',textfont_size = 12, textfont_color='#FFF'
                    )])


    trace1.update_layout(title=dict(text="Number of Crashes based on Geometry of Road in : {}".format(value),
                               font=dict(family='Sherif',
                                         size=20,
                                         color='#1f77b4')),
                    xaxis=dict(showgrid=False, tickfont=dict(color="#1f77b4"),fixedrange=True),
                    yaxis=dict(showgrid=False, showline=True, tickfont=dict(color="#1f77b4"),fixedrange=True),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)')

    return trace1


@app.callback(
    Output(component_id='dd-graph', component_property='figure'),
    [Input(component_id='dropdown1', component_property='value'),Input(component_id='dropdown_year', component_property='value')])
def update_value(value,value1):
    data_temp=data[(data['roaD_GEOMETRY']==value) & (data['year']== int(value1))]
    data_temp=data_temp.groupby(['speeD_ZONE']).sum().reset_index(),

    trace1= go.Scatter(x=data_temp[0]['speeD_ZONE'],y=data_temp[0]['totaL_PERSONS'], opacity=0.75, mode='lines',
                       line=dict(color='firebrick', width=4,dash='dot'))
    g = go.Figure(data=[trace1])
    g.update_layout(title=dict(text ="Crashes based on Speed limit in {} in the year {}".format(value,value1),
                               font =dict(family='Sherif',
                               size=20,
                               color = '#1f77b4')),
                    xaxis=dict(showgrid=False,tickfont=dict(color="#1f77b4")),
                    yaxis=dict(showgrid=False,showline = True,tickfont=dict(color="#1f77b4")),paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
    return g

@app.callback(
    Output(component_id='dd-graph3', component_property='figure'),
    [Input(component_id='dropdown_year', component_property='value')])
def update_value(value):
    crash_data = crash_data1[crash_data1['Year'] == value]
    temp = crash_data.groupby(['ROAD_GEOMETRY']).sum().reset_index()
    country = temp['ROAD_GEOMETRY']

    schools = country

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=temp['YOUNG_DRIVER'],
        x=schools,
        marker=dict(color="crimson", size=13),
        mode="markers",
        name="YOUNG DRIVERS"
    ))

    fig.add_trace(go.Scatter(
        y=temp['OLD_DRIVER'],
        x=schools,
        marker=dict(color="gold", size=13),
        mode="markers",
        name="OLD DRIVERS",
    ))

    fig.update_layout(

        title=dict(text='Number of people Injured based on Age and Geometry of Road in {}'.format(value),
                   font=dict(
                       family="Sherif",
                       size=20,
                       color="#1f77b4"
                   )
                   ),
        xaxis=dict(showgrid=False, tickfont=dict(color="#1f77b4")),
        yaxis=dict(showgrid=False, showline=True, tickfont=dict(color="#1f77b4")),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            traceorder="normal",
            font=dict(
                family="Sherif",
                size=12,
                color="#1f77b4"
            ),

            bordercolor="Black",
            borderwidth=2
        )
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)