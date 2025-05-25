import dash_bootstrap_components as dbc
from dash import html, dcc

from shared import header, region_filter, graph

layout = dbc.Container([
    header('Участники'),
    html.Br(),
    region_filter,

    graph(
        'Стаж вождения',
        'Водители с каким стажем чаще всего попадают в ДТП?',
        dcc.Graph(id='driving-experience'),
    ),

    graph(
        'Роли участников',
        'Какие участники дорожного движения чаще всего попадают в ДТП?',
        dbc.Col([
            dcc.Graph(id='participant-roles'),
        ], width=6),
        dbc.Col([
            dcc.Graph(id='participant-damage')
        ], width=6),
    ),

    graph(
        'Пол водителей',
        'Водители какого пола чаще всего попадали в ДТП?',
        dcc.Graph(id='driver-gender'),
    ),

    graph(
        'Нарушения',
        'Какие нарушения чаще всего совершают участники ДТП?',
        dbc.Col([
            dcc.Graph(id='participant-violations-1'),
        ], width=4),
        dbc.Col([
            dcc.Graph(id='participant-violations-2'),
        ], width=4),
        dbc.Col([
            dcc.Graph(id='participant-violations-3'),
        ], width=4),
    ),
])
