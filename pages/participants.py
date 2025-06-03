import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html, dcc, callback, Input, Output

from data import participants_df
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
])


@callback(
    Output('driving-experience', 'figure'),
    Output('participant-roles', 'figure'),
    Output('participant-damage', 'figure'),
    Output('driver-gender', 'figure'),
    Input('crossfilter-region', 'value'),
)
def update_participants(region):
    region_participants_df = participants_df[participants_df['region'].isin(region)]

    experience_figure = px.bar(
        region_participants_df
        .value_counts(subset=['years_of_driving_experience'])
        .reset_index(name='count')
        .sort_values('years_of_driving_experience'),

        x='years_of_driving_experience',
        y='count',
        orientation='v',

        labels={
            'years_of_driving_experience': 'Опыт вождения (лет)',
            'count': 'Количество ДТП',
        }
    )

    role_figure = px.pie(
        region_participants_df
        .value_counts(subset=['role'])
        .reset_index(name='count'),

        values='count',
        names='role',

        labels={
            'role': 'Роль',
            'count': 'Количество',
        }
    )

    damage_figure = px.bar(
        region_participants_df
        .value_counts(subset=['role', 'health_status'])
        .reset_index(name='count'),

        x='role',
        y='count',
        color='health_status',
        orientation='v',

        labels={
            'role': 'Роль',
            'health_status': 'Состояние здоровья',
            'count': 'Количество ДТП',
        }
    )

    gender_figure = px.bar(
        region_participants_df[region_participants_df['role'] == 'Водитель']
        .value_counts(subset=['gender', 'year'])
        .reset_index(name='count')
        .sort_values('year'),

        x='year',
        y='count',
        color='gender',
        orientation='v',

        labels={
            'year': 'Год',
            'gender': 'Пол',
            'count': 'Количество ДТП',
        }
    )

    return experience_figure, role_figure, damage_figure, gender_figure
