import dash_bootstrap_components as dbc
from dash import html, dcc

from shared import header, graph

layout = dbc.Container([
    header('Основное'),
    html.Br(),

    graph(
        'Участники ДТП',
        'Количество погибших и пострадавших в ДТП',
        dcc.Graph(id='total-participants'),
    ),

    graph(
        'Количество ДТП',
        'Количество произошедших ДТП за всё время',
        dcc.Graph(id='total-participants'),
    ),
])
