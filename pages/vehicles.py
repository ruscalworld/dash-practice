import dash_bootstrap_components as dbc
from dash import html, dcc

from shared import header, region_filter, graph

layout = dbc.Container([
    header('Транспортные средства'),
    html.Br(),
    region_filter,

    graph(
        'Возраст ТС',
        'Зависимость количества ДТП от года выпуска транспортного средства',
        dcc.Graph(id='vehicle-age'),
    ),

    graph(
        'Производители ТС',
        'Зависимость количества ДТП от марки транспортного средства',
        dcc.Graph(id='vehicle-brand'),
    ),

    graph(
        'Категории ТС',
        'Зависимость количества ДТП от вида транспортного средства',
        dcc.Graph(id='vehicle-category'),
    ),

    graph(
        'Вред здоровью и категории ТС',
        'Зависимость причинённого вреда здоровью от категории ТС, попавшего в ДТП',
        dcc.Graph(id='vehicle-category-injures'),
    ),
])
