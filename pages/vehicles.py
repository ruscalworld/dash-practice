import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc, callback, Input, Output

from data import vehicles_df
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
])


@callback(
    Output('vehicle-age', 'figure'),
    Output('vehicle-brand', 'figure'),
    Output('vehicle-category', 'figure'),
    Input('crossfilter-region', 'value'),
)
def update_vehicles(region):
    region_vehicles_df = vehicles_df[vehicles_df['region'].isin(region)]

    age_figure = px.bar(
        region_vehicles_df
        .value_counts(subset=['year'])
        .reset_index(name='count')
        .sort_values('year'),

        x='year',
        y='count',
        orientation='v',
        range_x=(1970, 2023),

        labels={
            'year': 'Год выпуска',
            'count': 'Количество ДТП',
        }
    )

    brand_figure = px.bar(
        region_vehicles_df
        .value_counts(subset=['brand'])
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(10),

        x='count',
        y='brand',
        orientation='h',

        labels={
            'brand': 'Марка',
            'count': 'Количество ДТП',
        }
    )

    category_figure = px.bar(
        region_vehicles_df
        .value_counts(subset=['category'])
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(10),

        x='count',
        y='category',
        orientation='h',
        text_auto='pop',

        labels={
            'category': 'Категория',
            'count': 'Количество ДТП',
        }
    )

    return age_figure, brand_figure, category_figure

