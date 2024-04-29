import dash
from dash import dcc, html, Input, Output, callback, State
from dash.exceptions import PreventUpdate
import dash_loading_spinners as dls

from edafunctions import get_seasons
from modelsfunctions import get_binary_model, get_binary_model_predict, get_circuits_data, get_inputs_params, get_pca_data, get_pca_graph, get_teams

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

pred_style = {
    'display': 'flex',
    'align-items': 'center',
    'gap': '10px',
    'justify-content': 'space-between',
    'width': '70%'
}

element_style = {
    'display': 'flex',
    'align-items': 'flex-end',
    'gap': '5px'
}

car = element_style
car['align-items'] = 'center'

dates = get_seasons()
dates = dates.sort_values(by='year', ascending=False)

pca_data = get_pca_data()
pca_variables = pca_data.columns[2:]

layout = html.Main([
    html.Nav([
        dcc.Tabs(
            id='tabs',
            value='binarylsm',
            children=[
                dcc.Tab(label='Binary Logistic Regression', value='binarylsm'),
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
                        html.Nav([
                            html.Article([
                                html.Span('Season', style={'font-weight': 'regular', 'color': 'rgba(255, 255, 255, 0.35)', 'margin-left': '12px', 'position': 'relative', 'top': '5px'}),
                                dcc.Dropdown(
                                    id='seasons-dropdown',
                                    options=[{'label': k, 'value': k} for i, k in enumerate(dates['year'])],
                                    value=dates['year'].max(),
                                    style={
                                        "color": "black", 
                                        "background-color": "transparent", 
                                        "border": "none", 
                                    },
                                ),
                            ], style={'width': '50%'}),
                            html.Article([
                                html.Span('Circuit', style={'font-weight': 'regular', 'color': 'rgba(255, 255, 255, 0.35)', 'margin-left': '12px', 'position': 'relative', 'top': '5px'}),
                                dcc.Dropdown(
                                    id='circuits-dropdown',
                                    style={
                                        "color": "black", 
                                        "background-color": "transparent", 
                                        "border": "none", 
                                    },
                                ),
                            ], style={'width': '50%'}) 
                        ], style={'width': '90%', 'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center', 'gap': '30px'}),
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
                                    autoComplete = 'off',
                                    style={"width": "50%", "color": "#007eff", "background-color": "transparent", "border": "none", "margin-top": "30px", "border-bottom": ".3px solid #e10600"}
                                ),
                                dcc.Input(
                                    type='number',
                                    id='minutes-binary',
                                    placeholder = 'Race duration in minutes...',
                                    autoComplete = 'off',
                                    style={"width": "50%", "color": "#007eff", "background-color": "transparent", "border": "none", "margin-top": "30px", "border-bottom": ".3px solid #e10600"}
                                ),
                            ], style={'display': 'flex', 'align-items': 'center', 'gap': '20px', 'margin-top': '30px'}),
                            html.Div([
                                dcc.Input(
                                    type='number',
                                    id='pits-binary',
                                    placeholder = '# of pit stops...',
                                    autoComplete = 'off',
                                    style={"width": "50%", "color": "#007eff", "background-color": "transparent", "border": "none", "margin-top": "30px", "border-bottom": ".3px solid #e10600"}
                                ),
                                dcc.Input(
                                    type='number',
                                    id='fastestlapspeed-binary',
                                    placeholder = 'Fastest lap speed in km/h...',
                                    autoComplete = 'off',
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
                                html.Div(
                                    id='prediction-result', 
                                    style={
                                        'margin-top': '30px',
                                        'display': 'flex',
                                        'flex-direction': 'column',
                                        'align-items': 'center',
                                        'gap': '10px'
                                    }
                                ),
                                color='#fff',
                                speed_multiplier=2,
                                show_initially=False
                            ),
                        ], style={'width': '90%', 'margin-top': '20px'})
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
                    'align-items': 'stretch',
                    'gap': '20px',
                }),
                html.Div([
                    html.Div([
                        dcc.Graph(figure=fig_thresh),
                    ],
                    style={
                        'display': 'flex',
                        'align-items': 'center',
                        'gap': '20px',
                        'background-color': 'rgba(0, 0, 0, 0.7)',
                        'border': '.5px solid #222',
                        'border-radius': '20px',
                        'padding': '20px',
                        'width': '40%',
                        'place-content': 'center'
                    }),
                    html.Div([
                        dcc.Graph(figure=fig_cm),
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
                    })
                ], 
                style={
                    'display': 'flex',
                    'align-items': 'stretch',
                    'gap': '20px',
                }),
                html.Div(
                    dcc.Graph(figure=fig_hist),
                    style={
                        'display': 'flex',
                        'align-items': 'center',
                        'gap': '20px',
                        'background-color': 'rgba(0, 0, 0, 0.7)',
                        'border': '.5px solid #222',
                        'border-radius': '20px',
                        'padding': '20px',
                        'width': '100%',
                        'place-content': 'center'
                    }
                )
            ], 
            style={
                'margin-top': '50px',
                'display': 'flex',
                'flex-direction': 'column',
                'gap': '20px'
            })
        ], 
        style={
            'margin-top': '20px'
        })
    elif tab == 'pca':
        return html.Article([
            html.H3('Ranking the best teams by principal components - PCA', style={'text-align': 'center', 'margin-top': '50px'}),
            html.Aside([
                html.Div([
                    html.Div([
                        html.Article([
                            html.Span(id='variables', style={'font-weight': 'regular', 'color': 'rgba(255, 255, 255, 0.35)', 'margin-left': '12px', 'position': 'relative', 'top': '5px'}),
                            dcc.Dropdown(
                                id='variables-dropdown',
                                options=[{'label': k, 'value': k} for i, k in enumerate(pca_variables)],
                                value=[pca_variables[0], pca_variables[1]],
                                style={
                                    "color": "black", 
                                    "background-color": "transparent", 
                                    "border": "none", 
                                    "border-bottom": ".2px solid #e10600",
                                    "visibility": "hidden"
                                },
                                multi=True
                            ),
                            dcc.Graph(id='pca-graph-2d', style={'margin-top': '30px'})
                        ], style={'width': '50%'}), 
                    ], style={'width': '90%', 'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center', 'gap': '30px'}),
                ],                   
                style={
                    'display': 'flex',
                    'align-items': 'center',
                    'gap': '20px',
                    'background-color': 'rgba(0, 0, 0, 0.7)',
                    'border': '.5px solid #222',
                    'border-radius': '20px',
                    'padding': '20px',
                    'width': '100%',
                    'place-content': 'center'
                }
                )
                ,
                html.Div([
                    dcc.Graph(id='pca-graph-3d'),
                ],
                style={
                    'display': 'flex',
                    'align-items': 'center',
                    'gap': '20px',
                    'background-color': 'rgba(0, 0, 0, 0.7)',
                    'border': '.5px solid #222',
                    'border-radius': '20px',
                    'padding': '20px',
                    'width': '100%',
                    'place-content': 'center'
                })
            ],
            style={
                'display': 'flex',
                'flex-direction': 'column',
                'align-items': 'center',
                'gap': '30px',
                'margin-top': '50px',
                'width': '100%',
                'place-content': 'center'
            })
        ])
    else:
        return html.Article([
            html.H3('Error')
        ])
    
@callback(
    Output('team-suggestions-list', 'children'),
    Input({'id': 'team-opt', 'type': 'searchteam'}, 'value'),
    State('seasons-dropdown', 'value'),
    prevent_initial_call = True
)
def suggest_teams(typing, season):
    teams = get_teams(season)
    all_teams = teams
    all_teams = all_teams['name'].unique()
    filtered_teams = [team for team in all_teams if typing.lower() in team.lower()]

    return [html.Option(value=team) for team in filtered_teams]

@callback(
    Output('circuits-dropdown', 'options'),
    Output('circuits-dropdown', 'value'),
    Input('seasons-dropdown', 'value') 
)
def get_circuits(season):
    circuits = get_circuits_data(season)
    options = [{'label': name, 'value': raceid} for name, raceid in zip(circuits['name'], circuits['raceid'])]
    return options, circuits['raceid'].values[0]

@callback(
    Output('grid-binary', 'min'),
    Output('grid-binary', 'max'),
    Output('minutes-binary', 'min'),
    Output('pits-binary', 'min'),
    Output('pits-binary', 'max'),
    Output('fastestlapspeed-binary', 'min'),
    Output('fastestlapspeed-binary', 'max'),
    Input('seasons-dropdown', 'value')
)
def update_binary_model_limits(season):
    params = get_inputs_params(season)
    grid_min = params['min_grid'].values[0]
    grid_max = params['max_grid'].values[0]
    minutes_min = params['min_minutes'].values[0]
    minutes_max = params['max_minutes'].values[0]
    pits_min = params['min_pit_stop'].values[0]
    pits_max = params['max_pit_stop'].values[0]
    fastestlapspeed_min = params['min_fastestlapspeed'].values[0]
    fastestlapspeed_max = params['max_fastestlapspeed'].values[0]

    return grid_min, grid_max, minutes_min, pits_min, pits_max, fastestlapspeed_min, fastestlapspeed_max

@callback(
    Output('prediction-result', 'children'),
    Output('grid-binary', 'value'),
    Output('minutes-binary', 'value'),
    Output('pits-binary', 'value'),
    Output('fastestlapspeed-binary', 'value'),
    Input('predict-button', 'n_clicks'),
    State({'id': 'team-opt', 'type': 'searchteam'}, 'value'),
    State('grid-binary', 'value'),
    State('minutes-binary', 'value'),
    State('pits-binary', 'value'),
    State('fastestlapspeed-binary', 'value'),
    State('seasons-dropdown', 'value'),
    State('circuits-dropdown', 'value'),
    prevent_initial_call=True,
    running=[
        (Output("predict-button", "disabled"), True, False)
    ]
)
def predict_constructor(n_clicks, team, grid, minutes, pits, fastestlapspeed, season, circuit):
    teams = get_teams(season)
    if n_clicks is None:
        return dash.no_update
    else:
        constructorid = teams[teams['name'] == team]['constructorid'].values[0]
        constructorurl = teams[teams['name'] == team]['url'].values[0]

        prediction = get_binary_model_predict(season, circuit, grid, minutes, constructorid, pits, fastestlapspeed)
        if prediction < 0.5:
            color = '#e10600'
        else:
            color = '#00e600'

        info = [
            html.H5('Prediction Results', style={'text-align': 'center'}),
            html.Span([
                html.Span([
                    html.Img(src=dash.get_asset_url('webicons/constructors.svg'), alt='constructors icon', style={'width': '20px'}),
                    html.A(
                        team,
                        href=constructorurl,
                        target="_blank",
                        rel="noopener noreferrer", 
                        style={'color': '#e10600', 'text-decoration': 'none'}
                    )
                ], style=car),
                html.Span([
                    html.Img(src=dash.get_asset_url('webicons/grid.svg'), alt='grid icon', style={'width': '15px'}),
                    html.Span(f'{grid}')
                ], style=element_style)
            ], style=pred_style),
            html.Span([
                html.Span([
                    html.Img(src=dash.get_asset_url('webicons/duration.svg'), alt='duration icon', style={'width': '15px'}),
                    html.Span(f'{minutes} mins')
                ], style=element_style),
                html.Span([
                    html.Img(src=dash.get_asset_url('webicons/pits.svg'), alt='pits icon', style={'width': '15px'}),
                    html.Span(f'{pits}')
                ], style=element_style)
            ], style=pred_style),
            html.Span([
                html.Span([
                    html.Img(src=dash.get_asset_url('webicons/speed.svg'), alt='speed icon', style={'width': '15px'}),
                    html.Span(f'{fastestlapspeed} km/h')
                ], style=element_style),
                html.Span([
                    html.Img(src=dash.get_asset_url('webicons/prob.svg'), alt='prob icon', style={'width': '15px'}),
                    html.Span(f'{round(prediction * 100, 2)}%', style={'color': color})
                ], style=element_style)
            ], style=pred_style),
        ]

        return info, None, None, None, None

@callback(
    Output('pca-graph-2d', 'figure'),
    Output('variables', 'children'),
    Output('pca-graph-3d', 'figure'),
    Input('variables-dropdown', 'value')
)
def update_pca_graph(variables):
    if variables is None:
        return dash.no_update
    
    pca_graph, pca_graph3d = get_pca_graph(tuple(variables))

    variables = ', '.join(pca_variables)

    return pca_graph, f'Variables: {variables}', pca_graph3d