import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
import plotly.io as pio
import plotly.express as px
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("WEG", className="display-4"),
        html.Hr(),
        html.P(
            "Dashboards do Projeto", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Projeto 1", href="/page-1", active="exact"),
                dbc.NavLink("Projeto 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
df = pd.read_csv(r'C:\Users\gusta\PycharmProjects\pythonProject\teste3.csv')
pio.templates.default = "ggplot2"
variables = df.columns
graph_op =[{'label': 'Bar Chart', 'value': 'bar'},{'label':'Line Chart', 'value':'line'},
                {'label':'Amostras ', 'value':'amostra'}, {'label':'Scatter', 'value':'scatter'}]
mat_op =[{'label': i, 'value': i} for i in variables]
app.layout = html.Div([sidebar,
    html.Div([
        html.Br(), html.Br(),
        dbc.Row(dbc.Col(html.P('Eixo X'), width={'size': 3, 'offset':10})),
        dbc.Row(dbc.Col(dcc.Dropdown(id='axx', options= mat_op,value= 'Material'), width={'size': 3, 'offset':8}))

    ]),
    html.Div([
        dbc.Row(dbc.Col(html.P('Eixo Y'), width={'size': 3, 'offset':10})),
        dbc.Row(dbc.Col(dcc.Dropdown(id='axy', options= mat_op,value= 'Projetos'),width={'size':3, 'offset':8}))
    ]),
html.Div([
        dbc.Row(dbc.Col(dcc.RadioItems(id='check', options= graph_op,value= 'bar'),width={'size':3, 'offset':8}))
        ]),
       dbc.Row(dbc.Col(dcc.Graph(id='graph_var'),width={'size':8, 'offset':4}))

])
@app.callback(
    Output('graph_var', 'figure'), [Input('axx', 'value'), Input('axy', 'value'), Input('check', 'value')]
)
def up_graph (eixox, eixoy, graph_choice):
    if graph_choice == 'scatter':
        return {
            'data': [go.Scatter(x=df[eixox], y=df[eixoy], text=df['Material'], mode='markers')],

            'layout': go.Layout(xaxis={'title': eixox}, yaxis={'title': eixoy},
                                margin={'l': 90, 'b': 60, 't': 10, 'r': 0})}

    elif graph_choice =='line':
        fig = px.line(df, x=eixox, y=eixoy)
        return fig
    elif graph_choice =='bar':
        fig = px.bar(df, x= eixox, y=eixoy, hover_name='Material')

        return fig
    elif graph_choice =='amostra':
        dff = [go.Histogram(x=df.Material)]
        fig = go.Figure(data=dff)
        return fig




if __name__ == '__main__':
    app.run_server(debug=True)