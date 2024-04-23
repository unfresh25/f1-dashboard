from dash import html
import dash

dash.register_page(__name__)

layout = html.Main(
    html.Section([
        html.Article([
            html.Span('Error 404'),
            html.H1('Meow!'),
            html.P([html.Span("We can't seem to find the page"), html.Br(), html.Span("you're looking for.")]),
            html.A(
                'Go Home',
                href='/',
                style = {'text-decoration': 'none'}
            )
        ], style = {'text-align': 'center'}),
        html.Article([
            html.Img(
                src='../assets/imgs/404.svg', 
                alt='404 Error', 
                style={
                    'height': '250px', 
                    'filter': 'invert(100%) sepia(0%) saturate(4%) hue-rotate(276deg) brightness(122%) contrast(100%)'
                },
                className='img404'
            ),
            html.Div(
                style = {
                    'height': '24px',
                    'background-color': 'hsla(38, 21%, 19%, .16)',
                    'margin': '0 auto',
                    'border-radius': '50%',
                    'filter': 'blur(7px)',
                },
                className='shadow'
            )
        ])
    ],
    style = {
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center',
        'gap': '5rem',
        'margin-top': '10rem'
    })
)