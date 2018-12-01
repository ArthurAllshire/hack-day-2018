# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

from data import Data


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    dcc.Input(id='repo-in', value='thedropbears/pypowerup', type='text'),

    dcc.Graph(
        id='fft-repo',
    )
])

data = Data()

@app.callback(
    dash.dependencies.Output('fft-repo', 'figure'),
    [dash.dependencies.Input('repo-in', 'value')])
def update_repo_plot(input_value):
    (repo_owner, repo_name) = input_value.split('/')
    freq, amp = data.get_frequency(repo_owner, repo_name)
    return {
            'data': [
                {'x': freq, 'y': amp, 'type': 'line'}            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }

if __name__ == '__main__':
    app.run_server(debug=True)
