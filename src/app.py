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
    dbc.NavLink("Home", href = "/", active = "exact"),
    dbc.NavLink("Exploratory Analysis", href = "/eda", active = "exact"),
    dbc.NavLink("Predictive Analysis", href = "/pa", active = "exact")
]

app.layout = html.Div([
    dcc.Location(id='url'),

    html.Header([
        html.A([
            html.Span([
                html.Span("F1 ", style={"color": "#e10600",}),
                html.Span("Dashboard", style={"color": "#fff",})
            ]),
        ], href="/", style = {"font-size": "20px", "font-weight": "600", "cursor": "pointer", "text-decoration": "none"}),

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
                    "Embark on an exhilarating journey through Formula 1 from 1950 to 2023, where we dissect a wealth of data to predict the intricate dance between race strategies, driver prowess, and circuit nuances. "
                ], style = {"width": "80%", "margin-top": "-20px"})
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