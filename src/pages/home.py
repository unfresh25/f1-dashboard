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
            html.Img(src='../assets/imgs/f1_car.avif', alt='Formula 1 Red Bull Car', style={'height': '569px'}),
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
                html.P([
                    html.Span("The project encompassed an exploratory data analysis focusing on team and driver dynamics, alongside the deployment of diverse models including time series analysis, logistic regression, and principal component analysis. You can find more information about this analysis in our quarto report "),
                    html.A('here.', href='https://unfresh25.github.io/f1-dashboard/site/', rel='noopener noreferrer', target='_blank', style={'color': 'inherit'}),
                ],style={
                    'margin-bottom': '1rem',
                }),
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
                html.P([
                    "The 'F1 Dashboard' project utilizes a comprehensive dataset sourced from ",
                    html.A('Kaggle, ', href='https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020', target='_blank', rel='noopener noreferrer', style={'color': 'inherit'}),
                    "encompassing detailed information spanning Formula 1 races, drivers, constructors, qualifying sessions, circuits, lap times, pit stops, and championships, dating back from the inaugural season in 1950 up to the latest records of the 2023 season."
                ],
                style={
                    'margin-bottom': '1rem',
                }),
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
               html.Img(src='../assets/imgs/jorge_avatar.svg', alt='Team members', style={'height': '200px', 'width': '200px', 'background-color': '#fff', 'border-radius': '100%', 'padding': '5px'}),
               html.Span("Jorge Borja Serrano", style={'margin-top': '15px'}),
               html.Span("Mg. Applied Statistics"),
           ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'}),

           html.Aside([
               html.Img(src='../assets/imgs/jose_avatar.svg', alt='Team members', style={'height': '200px', 'width': '200px', 'background-color': '#fff', 'border-radius': '100%', 'padding': '5px', 'transform': 'scaleX(-1)'}),
               html.Span("Jose Mercado Reyes", style={'margin-top': '15px'}),
               html.Span("Mg. Applied Statistics"),
           ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})
       ], style={"display": "flex", "justify-content": "space-around", "margin-top": "100px"}),
    ],
    style={
        'width': '75%',
        'margin': '0 auto',
        'margin-top': '100px',
    }),
])