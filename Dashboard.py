from dash import Dash, html, dash_table, dcc
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

import altair as alt
from vega_datasets import data

# Import data

path = "https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv"
df = pd.read_csv(path, sep=',')

# Preprocessing

df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

df.sort_values(by='trip_distance', inplace=True)

def get_weekday(dt):
    return dt.weekday() #.weekday() is a method

def get_hour(dt):
    return dt.hour

def get_dom(dt):
    return dt.day #.day is an attribute 

# Visualisations

mapbox_pickup = px.scatter_mapbox(df, lat="pickup_latitude", lon="pickup_longitude", hover_name="passenger_count",color='passenger_count', zoom=10, center=dict(lat=40.7, lon=-73.9))
mapbox_pickup.update_layout(mapbox_style="open-street-map")

mapbox_dropoff = px.scatter_mapbox(df, lat="dropoff_latitude", lon="dropoff_longitude", hover_name="passenger_count", color='passenger_count', zoom=10)
mapbox_dropoff.update_layout(mapbox_style="open-street-map")

scat = px.scatter(df, x='trip_distance', y='total_amount')

hist = px.histogram(df, x='trip_distance', nbins=100)

plot = go.Figure(data=[go.Scatter(
    y=df['tip_amount'],
    mode='lines',)
])
plot.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                    step="day",
                    stepmode="backward"),
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
    )
)

brush = alt.selection_interval(resolve='global')
base = alt.Chart(df).mark_point().encode(
    y='fare_amount',
    color=alt.condition(brush, 'Origin', alt.ColorValue('gray')),
).add_params(
    brush
).properties(
    width=250,
    height=250
)


# Dash app

app = Dash(__name__)
app.layout = [
    html.Div(style={'textAlign': 'center'}, children=[
        html.H1('NYC Uber Trips'),
        dash_table.DataTable(data=df.to_dict('records'), page_size=10),
        dcc.Graph(figure=mapbox_pickup),
        dcc.Graph(figure=mapbox_dropoff),
        dcc.Graph(figure=plot),
        dcc.Graph(figure=scat),
        html.Div([
            dcc.Graph(figure=mapbox_pickup),
            dcc.Graph(figure=hist),
            dcc.Graph(figure=mapbox_dropoff),
        ], id='output-container', style={
            'display': 'flex',
            }),    
    ])
]

# Run the app

if __name__ == '__main__':
    app.run(debug=True)
