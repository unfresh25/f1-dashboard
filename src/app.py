from dash import Dash, dcc, html, Input, Output, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
from plotly.subplots import make_subplots

import warnings
warnings.filterwarnings("ignore")

app = Dash(
        __name__, 
        external_stylesheets=[dbc.themes.CYBORG], 
        title="F1 Dashboard", 
        update_title=None
    )

server=app.server

Navigation_options = [
    dbc.NavLink("Home"),
    dbc.NavLink("Exploratory Analysis"),
    dbc.NavLink("Predictive Analysis")
]

app.layout = html.Div([
    dcc.Location(id='url'),

    html.Header([
        html.Span([
            html.Span("F1 ", style={"color": "#e10600",}),
            html.Span("Dashboard", style={"color": "#fff",})
        ], style = {"font-size": "28", "font-weight": "600"}),

        dbc.Nav(Navigation_options, vertical=False, pills=True, style={"justify-content": "flex-start", "gap": "150px", "font-weight": "400"}),
    ], style={"display": "flex", "gap": "185px", "align-items": "center", "margin-top": "30px"}),

    html.Section([
        html.Aside([
            html.Span([
                html.Div([
                    html.H4("Formula 1"),
                    html.Div(className='line')
                ], style={"display": "flex", "align-items": "center", "width": "100%"})
            ], style={"display": "flex", "width": "100%"}),

            html.Span([
                html.H1("Discover", style={"margin-top": "-20px"}),
                html.H1("Learn &", style={"margin-top": "-30px"}),
                html.H1("Predict", style={"margin-top": "-30px"}),
            ]),

            html.Span([
                html.P([
                    "From 1950 to 2023, we delve into the wealth of data to predict how diverse factors influence race outcomes. Utilizing advanced data visualization techniques, we unravel the complex dynamics between race strategies, driver performance, and circuit characteristics."
                ], style = {"width": "80%", "margin-top": "-30px"})
            ])
        ]),

        html.Aside([
            html.Img(src=app.get_asset_url('f1_car.avif'), alt='Formula 1 Red Bull Car', style={'height': '569px'}),
        ])
    ], style={"display": "flex", "gap": "119px", "align-items": "center" , "justify-content": "space-between", "margin-top": "120px", "margin-left": "56px", "margin-right": "55px"})
])

if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(debug=True, host='0.0.0.0', port=5000)