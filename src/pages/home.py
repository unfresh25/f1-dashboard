import dash
from dash import Dash, dcc, html

dash.register_page(__name__, path='/')

layout = html.Main([
    html.Section([
        html.Aside([
            html.Span([
                html.Div([
                    html.H4("Formula 1"),
                    html.Div(className='line')
                ], 
                style={
                    "display": "flex", 
                    "align-items": "center", 
                    "width": "100%"
                })
            ], style={"display": "flex", "width": "100%"}),

            html.Span([
                html.H1([html.H1("D", style={"color": "#e10600"}), "iscover"], style={"margin-top": "-20px", 'display': 'flex'}),
                html.H1([html.H1("L", style={"color": "#e10600"}), "earn ", html.H1("&", style={"color": "#e10600"})], style={"margin-top": "-30px", 'display': 'flex'}),
                html.H1([html.H1("P", style={"color": "#e10600"}), "redict"], style={"margin-top": "-30px", 'display': 'flex'}),
            ]),

            html.Span([
                html.P([
                    "Embark on an exhilarating journey through Formula 1 from 1950 to 2023, where we dissect a wealth of data to predict the intricate dance between race strategies, driver prowess, and circuit nuances. "
                ], style = {"width": "80%", "margin-top": "-20px"})
            ])
        ]),

        html.Aside([
            html.Img(src='../assets/f1_car.avif', alt='Formula 1 Red Bull Car', style={'height': '569px'}),
        ])
    ], 
    style={
        "display": "flex", 
        "gap": "119px", 
        "align-items": "center" , 
        "justify-content": "space-between", 
        "margin-top": "120px", 
        "margin-left": "56px", 
        "margin-right": "55px"
    }),

    html.Section([
        html.H2("About the project", style={'font-size': '34px', 'text-align': 'center', 'font-weight': '400'}),
        html.Ol([
            html.Div(
                style={
                    'position': 'absolute',
                    'width': '2px',
                    'height': '100%',  
                    'background-color': '#555',
                    'left': '0',
                    'top': '0',
                },
                children=[
                    html.Div(
                        style={
                            'position': 'absolute',
                            'width': '8px',
                            'height': '8px',
                            'background-color': '#555',
                            'border-radius': '50%',
                            'left': '-3px',
                            'top': '-4px',
                        }
                    )
                ]
            ),
            html.Li([
                html.H3(
                    "Application",
                ),
                html.P(
                    "The application is designed to provide a comprehensive overview of Formula 1 racing data, including race results, driver performance, and circuit information. The user can explore and analyze the data in various ways to gain insights into the drivers, races, and circuits of the world's most prestigious Formula 1 racing organization.",
                    style={
                        'margin-bottom': '1rem',
                    }
                ),
            ],
            style={
                'position': 'relative',
                'padding-left': '1rem'
            }),
            html.Div(
                style={
                    'position': 'absolute',
                    'width': '2px',
                    'height': '100%',  
                    'background-color': '#555',
                    'left': '0',
                    'top': '0',
                },
                children=[
                    html.Div(
                        style={
                            'position': 'absolute',
                            'width': '8px',
                            'height': '8px',
                            'background-color': '#555',
                            'border-radius': '50%',
                            'left': '-3px',
                            'top': '220px',
                        }
                    )
                ]
            ),

            html.Li([
                html.H3(
                    "Analysis",
                ),
                html.P(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec mattis eros. Phasellus tempus magna ut nibh dapibus, ut ornare risus varius. Praesent eget dignissim lectus. Fusce elementum sed nunc in molestie. Aliquam erat volutpat. Ut sit amet tortor magna. Donec pretium quam et ante pretium, sed sagittis leo volutpat.",
                    style={
                        'margin-bottom': '1rem',
                    }
                ),
            ],
            style={
                'position': 'relative',
                'padding-left': '1rem',
                'margin-top': '100px'
            }),

            html.Div(
                style={
                    'position': 'absolute',
                    'width': '2px',
                    'height': '100%',  
                    'background-color': '#555',
                    'left': '0',
                    'top': '0',
                },
                children=[
                    html.Div(
                        style={
                            'position': 'absolute',
                            'width': '8px',
                            'height': '8px',
                            'background-color': '#555',
                            'border-radius': '50%',
                            'left': '-3px',
                            'top': '440px',
                        }
                    )
                ]
            ),

            html.Li([
                html.H3(
                    "Dataset",
                ),
                html.P(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec mattis eros. Phasellus tempus magna ut nibh dapibus, ut ornare risus varius. Praesent eget dignissim lectus. Fusce elementum sed nunc in molestie. Aliquam erat volutpat. Ut sit amet tortor magna. Donec pretium quam et ante pretium, sed sagittis leo volutpat.",
                    style={
                        'margin-bottom': '1rem',
                    }
                ),
            ],
            style={
                'position': 'relative',
                'padding-left': '1rem',
                'margin-top': '100px'
            }),
        ],
        style={
            'margin': '0 auto',
            'margin-top': '50px',
            'border-style': 'bold',
            'border-color': '#555',
            'list-style-type': 'none',
            'padding-left': '1rem',
            'position': 'relative',
            'width': '75%'
        }),
    ],
    style={
        'width': '75%',
        'margin': '0 auto',
        'margin-top': '100px',
    }),

    html.Section([
       html.H2("About the team", style={'font-size': '34px', 'text-align': 'center', 'font-weight': '400'}),

       html.Article([
           html.Aside([
               html.Img(src='../assets/jorge_avatar.svg', alt='Team members', style={'height': '200px', 'width': '200px', 'background-color': '#fff', 'border-radius': '100%', 'padding': '5px'}),
               html.Span("Jorge Borja Serrano", style={'margin-top': '15px'}),
               html.Span("Mg. Applied Statistic"),
           ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}),

           html.Aside([
               html.Img(src='../assets/jorge_avatar.svg', alt='Team members', style={'height': '200px', 'width': '200px', 'background-color': '#fff', 'border-radius': '100%', 'padding': '5px', 'transform': 'scaleX(-1)'}),
               html.Span("Jose Mercado Reyes", style={'margin-top': '15px'}),
               html.Span("Mg. Applied Statistic"),
           ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})
       ], style={"display": "flex", "justify-content": "space-around", "margin-top": "100px"}),
    ],
    style={
        'width': '75%',
        'margin': '0 auto',
        'margin-top': '100px',
    }),
])