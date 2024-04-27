import dash
from dash import Dash, dcc, html, Input, Output, dash_table, DiskcacheManager, clientside_callback
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
from plotly.subplots import make_subplots
import diskcache

import warnings
warnings.filterwarnings("ignore")

cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

app = Dash(
    __name__, 
    external_stylesheets=[dbc.themes.CYBORG], 
    title="F1 Dashboard", 
    update_title=None,
    use_pages=True,
    background_callback_manager=background_callback_manager,
    suppress_callback_exceptions=True
)

app._favicon = "favicon.ico"

server=app.server

Navigation_options = [
    dbc.NavLink("Home", href = "/", active = "exact"),
    dbc.NavLink("Exploratory Analysis", href = "/eda", active = "exact"),
    dbc.NavLink("Predictive Analysis", href = "/models", active = "exact")
]

app.layout = html.Div([
    html.Header([
        html.A([
            html.Span([
                html.Span("F1 ", style={"color": "#e10600",}),
                html.Span("Dashboard", style={"color": "#fff",})
            ]),
        ], 
        href="/", 
        style = {
            "font-size": "20px", 
            "font-weight": "600", 
            "cursor": "pointer", 
            "text-decoration": "none"
        }),

        dbc.Nav(
            Navigation_options, 
            vertical=False, 
            pills=True, 
            style={
                "justify-content": "flex-start", 
                "gap": "150px", 
                "font-weight": "400"
            }
        ),
        html.A([
            html.Img(src=app.get_asset_url("webicons/github.svg"), style={"height": "25px", 'filter': 'invert(100%) sepia(0%) saturate(0%) hue-rotate(194deg) brightness(100%) contrast(102%)'})
        ], 
        href='https://github.com/unfresh25/f1-dashboard',
        rel='noopener noreferrer',
        target='_blank')
    ], 
    style={
        "display": "flex", 
        "gap": "185px", 
        "align-items": "center", 
        "margin-top": "30px"
    }),

    html.Div(className='circle'),
    html.Div(className='circle2'),
    html.Div(className='circle3'),
    html.Div(className='circle4'),

    dash.page_container,
    dcc.Location(id='url'),
    dcc.Store(id='changed_url', storage_type='session'),
    
    html.Hr(style={'margin-top': '100px'}),

    html.Footer([
        html.Article([
            html.Span([
                html.Span("F1 ", style={"color": "#e10600",}),
                html.Span("Dashboard", style={"color": "#fff",})
            ], style={'font-size': '28px', 'font-weight': '600'}),
            html.Span("Powered by Plotly & Dash")
        ], style={"display": "flex", "flex-direction": "column"}, className="footer-names"),
        html.Img(src="https://www.uninorte.edu.co/o/uninorte-theme/images/uninorte/footer_un/logo.png", style={"height": "50px"})
    ], style={"display": "flex", "justify-content": "space-between", "align-items": "center"}),

    html.Br(),
])

clientside_callback(
    """
    function(_) {
        return "uuid-" + ((new Date).getTime().toString(16) + Math.floor(1E7*Math.random()).toString(16));
    }
    """,
    Output('changed_url', 'data'),
    Input('url', 'href')
)

if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(debug=True, host='0.0.0.0', port=5000)