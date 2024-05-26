from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

df = pd.read_csv('30-70cancerChdEtc.csv', sep=',')
all_cont = df['Location'].unique()
all_sexes = df['Dim1'].unique()

layout = dbc.Container([
    html.Div([
        html.H1("Показатели стран мира"),
        html.P(
            "Анализ основных показателей смертиности от рака по странам мира с 2000 по 2016 годы."
            )
        ], style = {
            'backgroundColor': 'rgb(140, 130, 188)',
            'padding': '10px 5px'
        }),
    
    html.Div([
            html.Div([
                html.Label('Страны'),
                dcc.Dropdown(
                    id = 'crossfilter-cont',
                    options = [{'label': i, 'value': i} for i in all_cont],
                    value = ['Russian Federation'],
                    multi = True
                )
            ],
            style = {'width': '48%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Пол'),
                dcc.Dropdown(
                    id = 'crossfilter-sex',
                    options = [{'label': i, 'value': i} for i in all_sexes]
                )
            ],
            style = {'width': '48%',  'float': 'right', 'display': 'inline-block'}),
        ], style = {
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),
    
    html.Div(
            dcc.Slider(
                id = 'crossfilter-year',
                min = df['Period'].min(),
                max = df['Period'].max(),
                value = 2000,
                step = None,
                marks = {str(year):
                    str(year) for year in df['Period'].unique()}
                ),
            style = {'width': '95%', 'padding': '0px 20px 20px 20px'}
        ),
    
    html.Div(
        dcc.Graph(id = 'bar1'),
        style = {'width': '49%', 'display': 'inline-block'}
    ),
       
    html.Div(
        dcc.Graph(id = 'line1'),
        style = {'width': '49%', 'float': 'right', 'display': 'inline-block'}
    ),

    html.Div(
        dcc.Graph(id = 'choropleth1'),
        style = {'width': '100%', 'display': 'inline-block'}
    )

], fluid= True)


@callback(
    [Output('bar1', 'figure')],
    [Input('crossfilter-cont', 'value'),
    Input('crossfilter-sex', 'value'),
    Input('crossfilter-year', 'value')]
)
def update_stacked_area(continent, sex, period):
    filtered_data = df[(df['Period'] <= period) &
        (df['Location'].isin(continent)) &
        (df['Dim1'] == sex)]
    bar1 = px.bar(
        filtered_data,
        x = 'Period',
        y = 'First Tooltip',
        color = 'First Tooltip',
        )
    return [bar1]

@callback(
    [Output('line1', 'figure')],
    [Input('crossfilter-cont', 'value'),
    Input('crossfilter-sex', 'value'),
    Input('crossfilter-year', 'value')]
)
def update_scatter(continent, sex, period):
    filtered_data = df[(df['Period'] <= period) &
        (df['Location'].isin(continent)) &
        (df['Dim1'] == sex)]
    line1 = px.line(
        filtered_data,
        x = 'Period',
        y = 'First Tooltip',
        color = 'Location',
        title = "Значения показателя по странам",
        markers = True,
    )
    return [line1]


@callback(
    [Output('choropleth1', 'figure')],
    [Input('crossfilter-sex', 'value')]
)
def update_choropleth(indication):
    choropleth1 = px.choropleth(
        df,
        locations='Location',
        locationmode = 'country names',
        color='First Tooltip',
        hover_name='Location',
        title='Показатели по странам',
        color_continuous_scale=px.colors.sequential.BuPu,
        animation_frame='Period',
        height=650
        )
    return [choropleth1]