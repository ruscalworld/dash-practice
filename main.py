import logging
import os

import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Output, Input

from pages import main, participants, conditions, vehicles

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

external_stylesheets = [dbc.themes.YETI]
app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    use_pages=True,
    add_log_handler=False,
    logger=logging.getLogger(__name__),
)

app.config.suppress_callback_exceptions = True

sidebar_style = {
    'position': 'fixed',
    'top': 0,
    'right': 0,
    'bottom': 0,
    'left': 0,
    'width': '16rem',
    'padding': '2rem 1rem',
}

content_style = {
    'margin-left': '18rem',
    'margin-right': '2rem',
    'padding': '2rem 1rem',
}

sidebar = html.Div([
    html.H2('ДТП', className='display-6'),
    html.Hr(),
    html.P('На территории РФ с 2015 по 2023 годы', className='lead'),
    dbc.Nav(
        [
            dbc.NavLink('Основное', href='/', active='exact'),
            dbc.NavLink('Участники', href='/participants', active='exact'),
            dbc.NavLink('Условия', href='/conditions', active='exact'),
            dbc.NavLink('Транспортные средства', href='/vehicles', active='exact'),
        ],
        vertical=True,
        pills=True,
    )
], style=sidebar_style, className='bg-light')

content = html.Div(id='page-content', style=content_style)
app.layout = html.Div([dcc.Location(id='url'), sidebar, content])

pages = {
    '/': main.layout,
    '/participants': participants.layout,
    '/conditions': conditions.layout,
    '/vehicles': vehicles.layout,
}


def p404(pathname):
    return html.Div([
        html.H1('404', className='text-danger'),
        html.Hr(),
        html.P(f'The pathname {pathname} was not recognized.'),
    ], className='p3 bg-light rounded-3')


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
)
def render_page_content(pathname):
    return pages.get(pathname, p404(pathname))


if __name__ == '__main__':
    app.run(debug=os.getenv('ENVIRONMENT', 'development') != 'production')
