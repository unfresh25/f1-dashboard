import dash
from dash import dcc, html, Input, Output, callback
import os
from dotenv import load_dotenv
import psycopg2 as psy
from psycopg2 import Error

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

dash.register_page(__name__)

layout = html.Main([

    dcc.Graph(id='map-graph'),

    html.H3('Constructors'),
    html.Hr(id='xd'),
    html.Section([
        html.Article([

        ])
    ],
    style={
        'display': 'flex',
    })

], 
style={
    'width': '90%',
    'margin': '0 auto',
    'margin-top': '80px'
    }
)

# @callback(
#     Output('map-graph', 'figure'),
#     Input('xd', 'children')
# )
# def update_graph(value):
#     country_counts = records_data['circuit_country'].value_counts().reset_index()
#     country_counts.columns = ['circuit_country', 'num_races']

#     temp_df = pd.merge(records_data, country_counts, on='circuit_country')

#     fig = px.scatter_mapbox(temp_df, lat="circuit_lat", lon="circuit_lng", hover_name="race_name",
#                             hover_data={"raceid": True, "race_time_in_milliseconds": True, "general_fastest_lap_time": True},
#                             size="num_races",
#                             zoom=4)

#     fig.update_layout(mapbox_style="open-street-map")
#     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

#     fig.show()

# def connection_db() -> psy.extensions.connection:
#     try:
#         conn = psy.connect(DATABASE_URL)
#         return conn
#     except (Exception, Error) as e:
#         print('Error while connecting to PostgreSQL', e)


# def get_map_data():
#     conn = connection_db()
#     cur = conn.cursor()

