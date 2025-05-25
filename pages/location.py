import dash_bootstrap_components as dbc
from dash import html, dcc

from shared import header, region_filter, graph

layout = dbc.Container([
    header('Местоположение'),
    html.Br(),
    region_filter,

    graph(
        'Аварийность по регионам',
        'Регионы с наибольшей аварийностью на 1000 человек населения',
        dbc.Col([
            dcc.Graph(id='most-accidents-regions'),
        ], width=6),
        dbc.Col([
            dcc.Graph(id='accident-map'),
        ], width=6),
    ),

    graph(
        'Пострадавшие',
        'Регионы с наибольшим числом погибших и пострадавших на 1000 человек населения',
        dbc.Col([
            dcc.Graph(id='most-injured-regions'),
        ], width=6),
        dbc.Col([
            dcc.Graph(id='most-dead-regions'),
        ], width=6),
    ),

    graph(
        'Объекты',
        'Объекты, рядом с которыми чаще всего происходят ДТП',
        dcc.Graph(id='nearby-objects'),
    ),

    graph(
        'Категории',
        'Зависимость категорий ДТП от объектов, рядом с которыми они произошли',
        dcc.Graph(id='nearby-objects-categories'),
    ),
])
