import dash_bootstrap_components as dbc
from dash import html, dcc

from shared import header, region_filter, graph

layout = dbc.Container([
    header('Условия'),
    html.Br(),
    region_filter,

    dbc.Row([
        dbc.Col([
            graph(
                'Погодные условия',
                'При каких погодных условиях чаще всего происходят ДТП?',
                dcc.Graph(id='weather-conditions'),
            ),
        ], width=4),
        dbc.Col([
            graph(
                'Освещённость',
                'При какой освещённости чаще всего происходят ДТП?',
                dcc.Graph(id='light-conditions'),
            ),
        ], width=4),
        dbc.Col([
            graph(
                'Дорожные условия',
                'При каких дорожных условиях чаще всего происходят ДТП?',
                dcc.Graph(id='road-conditions'),
            ),
        ], width=4),
    ]),

    dbc.Row([
        dbc.Col([
            graph(
                'Время суток',
                'В какое время суток чаще всего происходят ДТП?',
                dcc.Graph(id='day-time'),
            ),
        ], width=6),
        dbc.Col([
            graph(
                'Время года',
                'В какое время года чаще всего происходят ДТП?',
                dcc.Graph(id='year-season'),
            ),
        ], width=6),
    ]),
])
