import dash
from dash import dcc, html, Input, Output, callback, State
from dash.exceptions import PreventUpdate
import dash_loading_spinners as dls

from modelsfunctions import get_binary_model, get_binary_model_predict, get_teams

import os
from dotenv import load_dotenv

import pandas as pd

dash.register_page(__name__, title='F1 Dashboard - Predictive Analysis')

score_card = {
    'display': 'flex',
    'flex-direction': 'column',
    'align-items': 'center',
    'gap': '5px',
    'font-size': '20px'
}

score_style = {
    'display': 'flex',
    'align-items': 'center',
    'gap': '20px',
    'background-color': 'rgba(0, 0, 0, 0.7)',
    'border': '.5px solid #222',
    'border-radius': '20px',
    'padding': '10px',
    'width': '20%',
    'place-content': 'center',
    'height': '90px'
}

teams = get_teams()

layout = html.Main([
    html.Nav([
        dcc.Tabs(
            id='tabs',
            value='binarylsm',
            children=[
                dcc.Tab(label='Binary Logistic Regression', value='binarylsm'),
                dcc.Tab(label='Time Series', value='timeserie'),
                dcc.Tab(label='PCA - Principal Components', value='pca')
            ]
        )
    ], style={'margin-top': '50px'}),
    html.Section(
        id = 'models-section'
    )
])

@callback(
    Output('models-section', 'children'),
    Input('tabs', 'value')
)
def set_model_tab(tab):
    if tab == 'binarylsm':
        precision, recall, f1, auc, fig_hist, fig_thresh, fig_roc, fig_cm = get_binary_model()
        return html.Article([
            html.H3('Would my team score?', style={'text-align': 'center', 'margin-top': '50px'}),
            html.Aside([
                html.Div([
                    html.Img(src=dash.get_asset_url('webicons/precision.svg'), alt='analysis icon', style={'width': '20px'}),
                    html.Span([
                        html.Span('Precision', style={'color': '#e10600'}),
                        html.Span(round(precision, 3), style={'font-weight': 'bold'})
                    ],
                    style=score_card)
                ],
                style=score_style),
                html.Div([
                    html.Img(src=dash.get_asset_url('webicons/recall.svg'), alt='analysis icon', style={'width': '20px'}),
                    html.Span([
                        html.Span('Recall', style={'color': '#e10600'}),
                        html.Span(round(recall, 3), style={'font-weight': 'bold'})
                    ],
                    style=score_card)
                ],
                style=score_style),
                html.Div([
                    html.Img(src=dash.get_asset_url('webicons/analysis.svg'), alt='analysis icon', style={'width': '20px'}),
                    html.Span([
                        html.Span('F1-Score', style={'color': '#e10600'}),
                        html.Span(round(f1, 3), style={'font-weight': 'bold'})
                    ],
                    style=score_card)
                ],
                style=score_style),
                html.Div([
                    html.Img(src=dash.get_asset_url('webicons/curve.svg'), alt='analysis icon', style={'width': '20px'}),
                    html.Span([
                        html.Span('AUC', style={'color': '#e10600'}),
                        html.Span(round(auc, 3), style={'font-weight': 'bold'})
                    ],
                    style=score_card)
                ],
                style=score_style),
            ],
            style={
                'display': 'flex',
                'align-items': 'center',
                'gap': '30px',
                'margin-top': '50px',
                'width': '100%',
                'place-content': 'center'
            }),
            html.Aside([
                html.Div([
                    html.Div([
                        dcc.Graph(figure=fig_roc),
                    ],
                    style={
                        'display': 'flex',
                        'align-items': 'center',
                        'gap': '20px',
                        'background-color': 'rgba(0, 0, 0, 0.7)',
                        'border': '.5px solid #222',
                        'border-radius': '20px',
                        'padding': '20px',
                        'width': '60%',
                        'place-content': 'center'
                    }),
                    html.Div([
                        html.H5('What is the info of your constructor?'),
                        html.Div([
                            html.Span([
                                dcc.Input(
                                    type='text',
                                    id=dict(type = 'searchteam', id = 'team-opt'),
                                    placeholder = 'Search a team...',
                                    persistence = False, 
                                    autoComplete = 'off',
                                    list = 'team-suggestions-list',
                                    style={"width": "100%", "color": "#007eff", "background-color": "transparent", "border": "none", "border-bottom": ".3px solid #e10600"}
                                ),
                            ], style={'display': 'flex', 'align-items': 'center'}),
                            html.Datalist(
                                id = 'team-suggestions-list',
                            ),
                            html.Div([
                                dcc.Input(
                                    type='number',
                                    id='grid-binary',
                                    placeholder = 'Grid position...',
                                    style={"width": "50%", "color": "#007eff", "background-color": "transparent", "border": "none", "margin-top": "30px", "border-bottom": ".3px solid #e10600"}
                                ),
                                dcc.Input(
                                    type='text',
                                    id='minutes-binary',
                                    placeholder = 'Race duration in minutes...',
                                    style={"width": "50%", "color": "#007eff", "background-color": "transparent", "border": "none", "margin-top": "30px", "border-bottom": ".3px solid #e10600"}
                                ),
                            ], style={'display': 'flex', 'align-items': 'center', 'gap': '20px', 'margin-top': '30px'}),
                            html.Div([
                                dcc.Input(
                                    type='number',
                                    id='pits-binary',
                                    placeholder = '# of pit stops...',
                                    style={"width": "50%", "color": "#007eff", "background-color": "transparent", "border": "none", "margin-top": "30px", "border-bottom": ".3px solid #e10600"}
                                ),
                                dcc.Input(
                                    type='number',
                                    id='fastestlapspeed-binary',
                                    placeholder = 'Fastest lap speed in km/h...',
                                    style={"width": "50%", "color": "#007eff", "background-color": "transparent", "border": "none", "margin-top": "30px", "border-bottom": ".3px solid #e10600"}
                                ),
                            ], style={'display': 'flex', 'align-items': 'center', 'gap': '20px', 'margin-top': '30px'}),
                            html.Div([
                                html.Button([
                                    html.Img(src=dash.get_asset_url('webicons/predict.svg'), alt='predict icon', style={'width': '20px'}),
                                    'Predict'
                                ], 
                                id='predict-button', 
                                style={
                                    'background-color': '#e10600', 
                                    'color': '#fff', 
                                    'border': 'none', 
                                    'border-radius': '10px', 
                                    'padding': '10px 20px', 
                                    'font-weight': 'bold', 
                                    'cursor': 'pointer',
                                    'display': 'flex',
                                    'align-items': 'center',
                                    'gap': '10px'
                                }),
                            ], style={'display': 'flex', 'align-items': 'center', 'gap': '20px', 'margin-top': '30px', 'place-content': 'center', 'margin-bottom': '20px'}),
                            dls.Grid(
                                html.Span(id='prediction-result', style={'color': '#e10600', 'margin-top': '30px'}),
                                color='#fff',
                                speed_multiplier=2,
                                show_initially=False
                            ),
                        ], style={'width': '90%'})
                    ],
                    style={
                        'display': 'flex',
                        'flex-direction': 'column',
                        'align-items': 'center',
                        'gap': '20px',
                        'background-color': 'rgba(0, 0, 0, 0.7)',
                        'border': '.5px solid #222',
                        'border-radius': '20px',
                        'padding': '20px',
                        'width': '40%',
                        'place-content': 'center'
                    })
                ], 
                style={
                    'display': 'flex',
                    'align-items': 'flex-start',
                    'gap': '20px',
                }),

                dcc.Graph(figure=fig_hist, style={'margin-top': '50px'}),
                dcc.Graph(figure=fig_thresh, style={'margin-top': '50px'}),
                dcc.Graph(figure=fig_cm, style={'margin-top': '50px'})
            ], 
            style={'margin-top': '50px'})
        ], 
        style={
            'margin-top': '20px'
        })
    elif tab == 'timeserie':
        return html.Article([
            html.H3('Time Series')
        ])
    elif tab == 'pca':
        return html.Article([
            html.H3('PCA - Principal Components')
        ])
    else:
        return html.Article([
            html.H3('Error')
        ])
    
@callback(
    Output('team-suggestions-list', 'children'),
    Input({'id': 'team-opt', 'type': 'searchteam'}, 'value'),
    prevent_initial_call = True
)
def suggest_teams(typing):
    all_teams = teams
    all_teams = all_teams['name'].unique()
    filtered_teams = [team for team in all_teams if typing.lower() in team.lower()]

    return [html.Option(value=team) for team in filtered_teams]

@callback(
    Output('prediction-result', 'children'),
    Input('predict-button', 'n_clicks'),
    Input({'id': 'team-opt', 'type': 'searchteam'}, 'value'),
    Input('grid-binary', 'value'),
    Input('minutes-binary', 'value'),
    Input('pits-binary', 'value'),
    Input('fastestlapspeed-binary', 'value'),
    prevent_initial_call=True,
    running=[
        (Output("predict-button", "disabled"), True, False)
    ]
)
def predict_constructor(n_clicks, team, grid, minutes, pits, fastestlapspeed):
    if n_clicks is None:
        return dash.no_update
    else:
        constructorid = teams[teams['name'] == team]['constructorid'].values[0]

        prediction = get_binary_model_predict(grid, minutes, constructorid, pits, fastestlapspeed)

        return f'The probability of the constructor getting score is {round(prediction), 4} and {round(prediction * 100), 2}%'