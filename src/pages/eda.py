import dash
from dash import dcc, html, Input, Output, callback
import dash_loading_spinners as dls

import os
from dotenv import load_dotenv

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from functions import convert_milliseconds, get_constructor_info, get_constructor_stats_info, get_constructor_stats_names, get_constructor_stats_table, get_constructor_status_info, get_driver_age_point_distribution_data, get_driver_status_info, get_map_data, get_constructors_data, get_sankey_data, get_seasons, random_color

load_dotenv()

MAPBOX_TOKEN = os.getenv('MAPBOX_TOKEN')

dash.register_page(__name__, title='F1 Dashboard - Exploratory Analysis')

dates = get_seasons()
dates = dates.sort_values(by='year', ascending=False)

constructor_names = get_constructor_stats_names('2023')

layout = html.Main([
    html.Section([
        dls.Grid([
            dcc.Graph(id='map-graph')
        ],
        color='#fff',
        speed_multiplier=2,
        show_initially=True
        )
    ],
    style={
        'background-color': 'rgba(0, 0, 0, 0.7)',
    }),

    html.Section([
        html.H3('Constructors'),
        html.Hr(),
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
            ])            
        ], style={'width': '200px'}),
        html.Section([
            html.Article([
                html.Aside([
                    html.Label('Fastest Constructor', style={'font-size': '12px'}),
                    html.Div([
                        html.Span(id='fastest-constructor', style={'font-size': '18px', 'font-weight': '600'}, className='team'),
                        html.Div([
                            html.Img(src='../assets/webicons/speed.svg', alt='speed icon', style={'width': '15px'}),
                            html.Span(id='fastest-constructor-speed', style={'color': '#fff', 'font-size': '16px', 'font-weight': '300'})
                        ],
                        style={
                            'display': 'flex',
                            'align-items': 'flex-end',
                            'gap': '10px'
                        }),
                    ],
                    style={
                        'display': 'flex',
                        'flex-direction': 'column',
                        'align-items': 'center',
                        'margin-top': '15px',
                        'margin-bottom': '15px',
                        'gap': '5px'
                    })
                ],
                style={
                    'border': '.5px solid #222',
                    'border-radius': '20px',
                    'padding': '10px',
                }),
                html.Aside([
                    html.Label('Most Winner Constructor', style={'font-size': '12px'}),
                    html.Div([
                        html.Span(id='most-winner-constructor', style={'font-size': '18px', 'font-weight': '600'}, className='team'),
                        html.Div([
                            html.Img(src='../assets/webicons/winner.svg', alt='winner icon', style={'width': '15px'}),
                            html.Span(id='most-winner-constructor-wins', style={'color': '#fff', 'font-size': '16px', 'font-weight': '300'})
                        ],
                        style={
                            'display': 'flex',
                            'align-items': 'flex-end',
                            'gap': '10px'
                        }),
                    ],
                    style={
                        'display': 'flex',
                        'flex-direction': 'column',
                        'align-items': 'center',
                        'margin-top': '15px',
                        'margin-bottom': '15px',
                        'gap': '5px'
                    })
                ],
                style={
                    'border': '.5px solid #222',
                    'border-radius': '20px',
                    'padding': '10px',
                    'margin-top': '20px'
                }),
                html.Aside([
                    html.Label('Most Problematic Constructor', style={'font-size': '12px'}),
                    html.Div([
                        html.Span(id='most-problematic-constructor', style={'font-size': '18px', 'font-weight': '600'}, className='team'),
                        html.Div([
                            html.Img(src='../assets/webicons/problematicteam.svg', alt='problematic icon', style={'width': '15px'}),
                            html.Span(id='most-problematic-constructor-problems', style={'color': '#fff', 'font-size': '16px', 'font-weight': '300'})
                        ],
                        style={
                            'display': 'flex',
                            'align-items': 'flex-end',
                            'gap': '10px'
                        }),
                    ],
                    style={
                        'display': 'flex',
                        'flex-direction': 'column',
                        'align-items': 'center',
                        'margin-top': '15px',
                        'margin-bottom': '15px',
                        'gap': '5px'
                    })
                ],
                style={
                    'border': '.5px solid #222',
                    'border-radius': '20px',
                    'padding': '10px',
                    'margin-top': '20px'
                }),
            ],
            style={
                "padding": "20px",
                "border-radius": "12px",
                "border": "1px solid rgba(255, 255, 255, 0.125)",
                "margin-top": "10px",
                "background-color": "rgba(0, 0, 0, 0.7)",
                "backdrop-filter": 'blur(5px)',
                'width': '30%',
                'place-content': 'center'
            }),

            html.Article([
                html.H5(id='race-point-distribution-title', style={'text-align': 'center'}),
                dls.Grid([
                    dcc.Graph(id='race-point-distribution-graph')
                ],
                color='#fff',
                speed_multiplier=2,
                show_initially=True
                )
            ],
            style={
                "padding": "20px",
                "border-radius": "12px",
                "border": "1px solid rgba(255, 255, 255, 0.125)",
                "margin-top": "10px",
                "background-color": "rgba(0, 0, 0, 0.7)",
                "backdrop-filter": 'blur(5px)',
                'width': '70%'
            }),
        ],
        style={
            'display': 'flex',
            'gap': '10px'
        }),
        html.Section([
            html.Article([
                html.H5(id='race-distribution-title', style={'text-align': 'center'}),
                dls.Grid([
                    dcc.Graph(id='race-distribution-graph')
                ],
                color='#fff',
                speed_multiplier=2,
                show_initially=True
                )
            ],
            style={
                "padding": "20px",
                "border-radius": "12px",
                "border": "1px solid rgba(255, 255, 255, 0.125)",
                "margin-top": "10px",
                "background-color": "rgba(0, 0, 0, 0.7)",
                "backdrop-filter": 'blur(5px)',
                'width': '100%'
            })
        ],
        style={
            'display': 'flex',
        }),
        html.Section([
            html.Article([
                html.H5(id='constructor-radar-status-title', style={'text-align': 'center'}),
                dls.Grid([
                    dcc.Graph(id='constructor-radar-status-graph')
                ],
                color='#fff',
                speed_multiplier=2,
                show_initially=True
                )
            ],
            style={
                "padding": "20px",
                "border-radius": "12px",
                "border": "1px solid rgba(255, 255, 255, 0.125)",
                "margin-top": "10px",
                "background-color": "rgba(0, 0, 0, 0.7)",
                "backdrop-filter": 'blur(5px)',
                'width': '70%'
            }),
            html.Article([
                html.H6('Constructor Stats', style={'text-align': 'center'}),
                html.Nav(
                    dcc.Dropdown(
                        id='constructor-selector',
                        options=[{'label': name, 'value': name} for i, name in enumerate(constructor_names['name'])],
                        value=constructor_names['name'][0],
                        style={
                            "color": "black", 
                            "background-color": "transparent", 
                            "border": "none", 
                        }
                    ),
                    style={'margin-top': '20px'}
                ),
                dls.Grid([
                    html.H5(id='constructor-name', style={'margin-top': '25px', 'text-align': 'center'}),
                    html.Hr(),
                    html.Aside([
                        html.Span([
                            html.Label('Drivers'),
                            html.Div([
                                html.Img(src='../assets/webicons/f1car.svg', alt='driver icon', style={'width': '15px'}),
                                html.Span(id='constructor-total-drivers')
                            ],
                            style={
                                'display': 'flex',
                                'align-items': 'flex-end',
                                'gap': '10px'
                            }),
                        ],
                        style={
                            'display': 'flex',
                            'flex-direction': 'column',
                            'align-items': 'center',
                            'gap': '5px'
                        }),
                        html.Span([
                            html.Label('Speed'),
                            html.Div([
                                html.Img(src='../assets/webicons/speed.svg', alt='speed icon', style={'width': '15px'}),
                                html.Span(id='constructor-max-speed')
                            ],
                            style={
                                'display': 'flex',
                                'align-items': 'flex-end',
                                'gap': '10px'
                            }),
                        ],
                        style={
                            'display': 'flex',
                            'flex-direction': 'column',
                            'align-items': 'center',
                            'gap': '5px'
                        }),
                        html.Span([
                            html.Label('Points'),
                            html.Div([
                                html.Img(src='../assets/webicons/points.svg', alt='points icon', style={'width': '15px'}),
                                html.Span(id='constructor-total-points')
                            ],
                            style={
                                'display': 'flex',
                                'align-items': 'flex-end',
                                'gap': '10px'
                            }),
                        ],
                        style={
                            'display': 'flex',
                            'flex-direction': 'column',
                            'align-items': 'center',
                            'gap': '5px'
                        }),
                        html.Span([
                            html.Label('Wins'),
                            html.Div([
                                html.Img(src='../assets/webicons/winner.svg', alt='wins icon', style={'width': '15px'}),
                                html.Span(id='constructor-total-wins')
                            ],
                            style={
                                'display': 'flex',
                                'align-items': 'flex-end',
                                'gap': '10px'
                            }),
                        ],
                        style={
                            'display': 'flex',
                            'flex-direction': 'column',
                            'align-items': 'center',
                            'gap': '5px'
                        }),
                    ],
                    style={
                        'display': 'flex',
                        'gap': '20px',
                        'justify-content': 'space-between',
                    }),
                    dash.dash_table.DataTable(
                        id='constructor-stats-table',
                        style_cell={
                            "backgroundColor": "transparent",
                            "color": "gray",
                            "border": "0.5px solid #666",
                            "font-size": "16px",
                            "textAlign": "center",
                            'font-size': '14px'
                        },
                        style_data={
                            "whiteSpace": "normal",
                            "height": "auto",    
                        },
                        style_table={
                            'font-size': '12px',
                            'margin-top': '30px'
                        },
                        style_header={
                            "border": "0.5px solid #666",
                        }
                        )
                ],
                color='#fff',
                speed_multiplier=2,
                show_initially=True
                )
            ],
            style={
                "padding": "20px",
                "border-radius": "12px",
                "border": "1px solid rgba(255, 255, 255, 0.125)",
                "margin-top": "10px",
                "background-color": "rgba(0, 0, 0, 0.7)",
                "backdrop-filter": 'blur(5px)',
                'width': '30%'
            }),
        ],
        style={
            'display': 'flex',
            'gap': '10px'
        })
    ],
    style={
        'margin-top': '50px'
    }),

    html.Section([
        html.H3('Drivers'),
        html.Hr(),
        html.Section([
            html.Article([
                html.H5(id='driver-age-point-distribution-title', style={'text-align': 'center'}),
                dls.Grid([
                    dcc.Graph(id='driver-age-point-distribution-graph')
                ],
                color='#fff',
                speed_multiplier=2,
                show_initially=True
                )
            ],
            style={
                "padding": "20px",
                "border-radius": "12px",
                "border": "1px solid rgba(255, 255, 255, 0.125)",
                "margin-top": "10px",
                "background-color": "rgba(0, 0, 0, 0.7)",
                "backdrop-filter": 'blur(5px)',
                'width': '60%'
            }),
            html.Article([
                html.H5(id='driver-radar-status-title', style={'text-align': 'center'}),
                dls.Grid([
                    dcc.Graph(id='driver-radar-status-graph')
                ],
                color='#fff',
                speed_multiplier=2,
                show_initially=True
                )
            ],
            style={
                "padding": "20px",
                "border-radius": "12px",
                "border": "1px solid rgba(255, 255, 255, 0.125)",
                "margin-top": "10px",
                "background-color": "rgba(0, 0, 0, 0.7)",
                "backdrop-filter": 'blur(5px)',
                'width': '40%',
                'place-content': 'center'
            }),
        ],
        style={
            'display': 'flex',
            'gap': '10px'
        }),
    ],
    style={
        'margin-top': '50px'
    })
], 
style={
    'width': '90%',
    'margin': '0 auto',
    'margin-top': '50px'
    }
)

@callback(
    Output('map-graph', 'figure'),
    Input('seasons-dropdown', 'value')
)
def update_map_graph(value):
    records_data = get_map_data(value)

    records_data['race_time'] = records_data['race_time_in_milliseconds'].apply(convert_milliseconds) 

    country_counts = records_data['circuit_country'].value_counts().reset_index()
    country_counts.columns = ['circuit_country', 'num_races']

    temp_df = pd.merge(records_data, country_counts, on='circuit_country')

    fig = px.scatter_mapbox(
        temp_df, lat='circuit_lat', lon='circuit_lng', hover_name='race_name',
        hover_data={'num_races': False, 'Race Duration': records_data['race_time'], 'Fastest Lap Speed': (temp_df['fastest_lap_speed'].astype(str)+ ' km/h'), 'circuit_lat': False, 'circuit_lng': False},
        size='num_races',
        zoom=2,
        title='Countries with most races',
    )


    fig.update_layout(
        mapbox = dict(center= dict(lat=52.370216, lon=4.895168),            
        accesstoken=MAPBOX_TOKEN,
        style="dark"
    ))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

@callback(
    Output('fastest-constructor', 'children'),
    Output('fastest-constructor-speed', 'children'),
    Output('most-winner-constructor', 'children'),
    Output('most-winner-constructor-wins', 'children'),
    Output('most-problematic-constructor', 'children'),
    Output('most-problematic-constructor-problems', 'children'),
    Input('seasons-dropdown', 'value')
)
def update_stats(value):
    fastest_constructor, most_winner_constructor, most_problematic_constructor = get_constructor_info(value)
    
    fastest_constructor_name = html.A(f"{fastest_constructor.name[0]}", href=f"{fastest_constructor.url[0]}", target="_blank", rel='noopener noreferrer', style={'text-decoration': 'none', 'color': '#e10600'})
    fastest_constructor_speed = f'{fastest_constructor.speed[0]} km/h'
    most_winner_constructor_name = html.A(f'{most_winner_constructor.name[0]}', href=f'{most_winner_constructor.url[0]}', target="_blank", rel='noopener noreferrer', style={'text-decoration': 'none', 'color': '#e10600'})
    most_winner_constructor_wins = f'{int(most_winner_constructor.wins[0])} wins'
    most_problematic_constructor_name = html.A(f'{most_problematic_constructor.name[0]}', href=f'{most_problematic_constructor.url[0]}', target="_blank", rel='noopener noreferrer', style={'text-decoration': 'none', 'color': '#e10600'})
    most_problematic_constructor_problems = f'{int(most_problematic_constructor.problems[0])} problems'

    return fastest_constructor_name, fastest_constructor_speed, most_winner_constructor_name, most_winner_constructor_wins, most_problematic_constructor_name, most_problematic_constructor_problems
    
@callback(
    Output('race-distribution-graph', 'figure'),
    Output('race-distribution-title', 'children'),
    Output('race-point-distribution-graph', 'figure'),
    Output('race-point-distribution-title', 'children'),
    Input('seasons-dropdown', 'value')
)
def update_constructors_graphs(value):
    records_data = get_constructors_data(value)

    fig = go.Figure()

    races = records_data['race_name'].unique()
    
    top_constructors = records_data[records_data['race_name'] == races[-1]].head(5)

    for constructor in records_data['constructor_name'].unique():
        constructor_data = records_data[records_data['constructor_name'] == constructor]
        fig.add_trace(go.Scatter(x=races, y=constructor_data['total_points'],
                                mode='lines', name=constructor))

    fig.update_layout(
        xaxis=dict(title='Carrera'),
        yaxis=dict(title='Puntos acumulados'),
        showlegend=True
    )

    fig.update_traces(hovertemplate=None)
    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_xaxes(visible=False, showticklabels=False)
    fig.update_layout(hovermode="x unified")
    fig.update_layout(
        margin={'b': 0, 'r': 30, 'l': 30, 't': 0},
        xaxis={'gridcolor': '#111', 'tickfont': {'color': 'white'}},
        yaxis={'gridcolor': '#111', 'tickfont': {'color': 'white'}},
        plot_bgcolor='rgba(0, 0, 0, 0.0)',
        paper_bgcolor='rgba(0, 0, 0, 0.0)',
        font_color="white",
        hoverlabel=dict(
            bgcolor="#111"
        )
    )

    text = [f"{i+1}. {row['constructor_name']}: {row['total_points']} puntos" for i, (_, row) in enumerate(top_constructors.iterrows(), start=0)]
    annotation_spacing = 0.03

    for i, annotation_text in enumerate(text):
        fig.add_annotation(
            xref="paper",
            yref="paper",
            x=0,
            y=1 - i * annotation_spacing,
            text=annotation_text,
            showarrow=False,
            font=dict(size=12),
            align='left'
        )

    results = get_sankey_data(value)

    nodes = {'Puntos': 0}
    constructors = {}
    drivers = {}
    links = []

    node_labels = ['Puntos']
    node_values = [0]

    for row in results:
        constructor_id, constructor_ref, constructor_name, constructor_nationality, driver_name, points = row
        
        if constructor_name not in nodes:
            nodes[constructor_name] = len(nodes)
            node_labels.append(constructor_name)
            node_values.append(0)
        
        if driver_name not in nodes:
            nodes[driver_name] = len(nodes)
            node_labels.append(driver_name)
            node_values.append(0)
        
        node_values[nodes[constructor_name]] += points
        node_values[nodes[driver_name]] += points
        
        links.append({
            'source': nodes['Puntos'],
            'target': nodes[constructor_name],
            'value': points,
            'color': random_color()
        })
        
        links.append({
            'source': nodes[constructor_name],
            'target': nodes[driver_name],
            'value': points,
            'color': random_color()
        })

    fig2 = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=node_labels,
            color=[random_color() for _ in range(len(nodes))],
            customdata=node_values,
            hovertemplate='%{label}: %{customdata} puntos<br>',
        ),
        link=dict(
            source=[link['source'] for link in links],
            target=[link['target'] for link in links],
            value=[link['value'] for link in links],
            color=[link['color'] for link in links]
        )
    )])

    fig2.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0.0)',
        paper_bgcolor='rgba(0, 0, 0, 0.0)',
        font_color="white"
    )

    constructor_standings = f'Constructor standings in the {value} season'
    top_sankey_constructors = f'Top constructor and drivers by points accumulated since the {value} season'

    return fig, constructor_standings, fig2, top_sankey_constructors

@callback(
    Output('constructor-radar-status-title', 'children'),
    Output('constructor-radar-status-graph', 'figure'),
    Input('seasons-dropdown', 'value'),
    Input('constructor-selector', 'value')
)
def update_constructor_radar_status_graph(value, constructor):
    records_data = get_constructor_status_info(value, constructor)
    fig = go.Figure(data=go.Scatterpolar(
      r=records_data['problems'],
      theta=records_data['status'],
      fill='toself',
      name='Constructor problems',
      fillcolor='rgba(225, 6, 0, 0.5)',
      line=dict(color='rgba(225, 6, 0, 0.5)')
    ))

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0.0)',
        paper_bgcolor='rgba(0, 0, 0, 0.0)',
        font_color="white",
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 20]
            ),
            bgcolor='rgba(0, 0, 0, 0.0)'
        )
    )
    
    return f'{constructor} races status in the {value} season', fig

@callback(
    Output('constructor-selector', 'options'),
    Output('constructor-selector', 'value'),
    Input('seasons-dropdown', 'value'),
    prevent_initial_call=True
)
def update_constructor_selector(value):
    constructor_names = get_constructor_stats_names(value)
    options = [{'label': name, 'value': name} for i, name in enumerate(constructor_names['name'])]
    value = constructor_names['name'][0]
    return options, value

@callback(
    Output('constructor-name', 'children'),
    Output('constructor-total-drivers', 'children'),
    Output('constructor-max-speed', 'children'),
    Output('constructor-total-points', 'children'),
    Output('constructor-total-wins', 'children'),
    Input('seasons-dropdown', 'value'),
    Input('constructor-selector', 'value')
)
def update_constructor_stats(value, constructor_name):
    records_data = get_constructor_stats_info(value, constructor_name)
    return records_data['name'][0], records_data['total_drivers'][0], records_data['max_speed'][0], records_data['total_points'][0], records_data['total_wins'][0]

@callback(
    Output('constructor-stats-table', 'data'),
    Output('constructor-stats-table', 'columns'),
    Input('seasons-dropdown', 'value'),
    Input('constructor-selector', 'value')
)
def update_constructor_stats_table(value, constructor_name):
    records_data = get_constructor_stats_table(value, constructor_name)
    records_data.rename(columns={'surname': 'Driver', 'max_speed': 'Speed', 'total_points': 'Points', 'total_wins': 'Wins'}, inplace=True)
    columns = [{'name': col, 'id': col} for col in records_data.columns]

    return records_data.to_dict('records'), columns

@callback(
    Output('driver-age-point-distribution-title', 'children'),
    Output('driver-age-point-distribution-graph', 'figure'),
    Input('constructor-selector', 'value'),
    Input('seasons-dropdown', 'value')
)
def update_driver_age_point_distribution_graph(constructor_name, year):
    records_data = get_driver_age_point_distribution_data(constructor_name, year)

    fig = go.Figure()

    ages = records_data['age'].unique()

    for driver in records_data['driver'].unique():
        driver_data = records_data[records_data['driver'] == driver]
        fig.add_trace(go.Scatter(x=ages, y=driver_data['points'],
                                mode='lines', name=driver,
                                hovertemplate='<b>%{text}</b><extra></extra>',
                                text=[f"{driver_data['constructor'].iloc[i]}" for i in range(len(driver_data))]))

    fig.update_layout(
        xaxis=dict(title='Edad'),
        yaxis=dict(title='Puntos acumulados'),
        showlegend=True
    )

    fig.update_traces(hovertemplate=None)
    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_xaxes(visible=False, showticklabels=False)
    fig.update_layout(hovermode="x unified")
    fig.update_layout(
        margin={'b': 0, 'r': 30, 'l': 30, 't': 0},
        xaxis={'gridcolor': '#111', 'tickfont': {'color': 'white'}},
        yaxis={'gridcolor': '#111', 'tickfont': {'color': 'white'}},
        plot_bgcolor='rgba(0, 0, 0, 0.0)',
        paper_bgcolor='rgba(0, 0, 0, 0.0)',
        font_color="white",
        hoverlabel=dict(
            bgcolor="#111"
        )
    )

    title = f'{constructor_name} drivers in {year}, distribution of points earned throughout their entire careers'

    return title, fig

@callback(
    Output('driver-radar-status-title', 'children'),
    Output('driver-radar-status-graph', 'figure'),
    Input('seasons-dropdown', 'value'),
    Input('constructor-selector', 'value')
)
def update_driver_radar_status_graph(value, constructor):
    records_data = get_driver_status_info(value, constructor)

    fig = go.Figure()

    drivers = records_data['surname'].unique()

    for driver in drivers:
        driver_data = records_data[records_data['surname'] == driver]
        colorf = random_color()
        fig.add_trace(go.Scatterpolar(
            r=driver_data['problems'],
            theta=driver_data['status'],
            fill='toself',
            name=driver,
            fillcolor=colorf,
            line=dict(color=colorf)
        ))

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0.0)',
        paper_bgcolor='rgba(0, 0, 0, 0.0)',
        font_color="white",
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 20]
            ),
            bgcolor='rgba(0, 0, 0, 0.0)'
        )
    )
    
    return f'Drivers races status in the {value} season from {constructor} team', fig