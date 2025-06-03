import logging

import dash_bootstrap_components as dbc
from dash import html, dcc

from data import accidents_df

logger = logging.Logger(__name__)

regions = accidents_df['region'].unique()
logger.info('loaded unique regions')

region_filter = dbc.Row([
    dbc.Col([
        html.P('Выберите регион'),
    ], width=2),

    dbc.Col([
        dcc.Dropdown(
            id='crossfilter-region',
            options=[{'label': i, 'value': i} for i in regions],
            value=[regions[0]],
            multi=True,
            searchable=True,
        ),
    ], width=3),
])


def header(title: str):
    return dbc.Row([
        dbc.Col([
            html.Div([
                html.H1(title),
                html.Hr(style={'color': 'black'}),
            ], style={'text-align': 'center'}),
        ]),
    ])


def graph(title: str, description: str, *args):
    return dbc.Stack([
        html.Div([
            html.H3(title),
            html.Small(description),
        ]),
        dbc.Row(args),
    ], gap=8, style={'margin': '16px 0'})
