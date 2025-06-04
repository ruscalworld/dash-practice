import logging

import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc

from data import participants_df, accidents_df, geojson
from shared import header, graph

logger = logging.Logger(__name__)


def total_participants_figure():
    total_participants = px.line(
        participants_df
        .value_counts(subset=['year', 'health_status'])
        .reset_index(name='count')
        .sort_values(by='year'),

        x='year',
        y='count',
        line_group='health_status',
        color='health_status',

        labels={
            'year': 'Год',
            'count': 'Количество',
            'health_status': 'Состояние',
        },
    )

    return total_participants


def total_accidents_figure():
    total_accidents = px.line(
        accidents_df
        .value_counts(subset=['year'])
        .reset_index(name='count')
        .sort_values(by='year'),

        x='year',
        y='count',
    )

    return total_accidents


def region_stats():
    absolute_accidents_df = accidents_df.value_counts(subset=['region', 'population']).reset_index(name='count')
    absolute_accidents_df['count_per_population'] = absolute_accidents_df['count'] / (absolute_accidents_df['population'] / 1000)
    absolute_accidents_df.sort_values('count_per_population', ascending=True, inplace=True)
    logger.info('completed region stats calculation')

    return px.bar(
        absolute_accidents_df.head(10),

        x='count_per_population',
        y='region',
        orientation='h',

        labels={
            'region': 'Регион',
            'count_per_population': 'Количество на 1000 чел.',
        }
    )


def region_map():
    absolute_accidents_df = (accidents_df.value_counts(subset=['region', 'geojson_region', 'population'])
                             .reset_index(name='count'))

    absolute_accidents_df['count_per_population'] = absolute_accidents_df['count'] / (absolute_accidents_df['population'] / 1000)
    logger.info('completed region map calculation')

    figure = px.choropleth(
        absolute_accidents_df[['region', 'geojson_region', 'count_per_population']],

        locations='geojson_region',
        geojson=geojson,
        featureidkey='properties.name',
        color='count_per_population',
        fitbounds='geojson',
        projection='mercator',
        center={'lat': 61.5240, 'lon': 105.3188},
        scope='asia',
        basemap_visible=False,

        labels={
            'geojson_region': 'Регион',
            'count_per_population': 'Количество ДТП на 1000 чел.',
        }
    )

    return figure


layout = dbc.Container([
    header('Основное'),
    html.Br(),

    graph(
        'Участники ДТП',
        'Количество погибших и пострадавших в ДТП',
        dcc.Graph(id='total-participants', figure=total_participants_figure()),
    ),

    graph(
        'Количество ДТП',
        'Количество произошедших ДТП за всё время',
        dcc.Graph(id='total-accidents', figure=total_accidents_figure()),
    ),

    graph(
        'Аварийность по регионам',
        'Регионы с наибольшей аварийностью на 1000 человек населения',
        dcc.Graph(id='most-accidents-regions', figure=region_stats()),
        dcc.Graph(id='accident-map', figure=region_map()),
    ),
])
