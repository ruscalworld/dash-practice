import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc, callback, Input, Output

from data import accidents_df
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
        ], width=6),
        dbc.Col([
            graph(
                'Освещённость',
                'При какой освещённости чаще всего происходят ДТП?',
                dcc.Graph(id='light-conditions'),
            ),
        ], width=6),
    ]),

    dbc.Row([
        graph(
            'Общие условия',
            'При какой погоде и освещённости чаще всего происходят ДТП?',
            dcc.Graph(id='conditions-summary'),
        ),
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


@callback(
    Output('weather-conditions', 'figure'),
    Output('light-conditions', 'figure'),
    Output('conditions-summary', 'figure'),
    Output('day-time', 'figure'),
    Output('year-season', 'figure'),
    Input('crossfilter-region', 'value'),
)
def update_conditions(region):
    region_accidents_df = accidents_df[accidents_df['region'].isin(region)]

    weather_figure = px.pie(
        region_accidents_df
        .value_counts(subset=['weather'])
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(5),

        values='count',
        names='weather',

        labels={
            'weather': 'Погода',
            'count': 'Количество ДТП',
        }
    )

    weather_figure.update_layout(legend={
        'yanchor': 'top',
        'y': 0.99,
        'xanchor': 'right',
        'x': 0.01,
    })

    light_figure = px.pie(
        region_accidents_df
        .value_counts(subset=['light'])
        .reset_index(name='count'),

        values='count',
        names='light',

        labels={
            'light': 'Освещённость',
            'count': 'Количество ДТП',
        }
    )

    light_figure.update_layout(showlegend=False)

    conditions_figure = px.scatter(
        region_accidents_df
        .value_counts(subset=['weather', 'light'])
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(10),

        x='weather',
        y='light',
        size='count',

        labels={
            'light': 'Освещение',
            'weather': 'Погода',
            'count': 'Количество ДТП',
        }
    )

    day_time_figure = px.bar(
        region_accidents_df
        .value_counts(subset=['hour'])
        .reset_index(name='count')
        .sort_values('hour'),

        x='hour',
        y='count',
        orientation='v',

        labels={
            'hour': 'Час дня',
            'count': 'Количество ДТП',
        }
    )

    months_figure = px.bar(
        region_accidents_df
        .value_counts(subset=['month'])
        .reset_index(name='count')
        .sort_values('month'),

        x='month',
        y='count',
        orientation='v',

        labels={
            'month': 'Месяц',
            'count': 'Количество ДТП',
        }
    )

    return weather_figure, light_figure, conditions_figure, day_time_figure, months_figure
