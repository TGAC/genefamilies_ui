from dash import Dash, dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc

import requests

import json

import pandas as pd

from .plotly_tree import (
    create_tree,
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


table_header = [
    html.Thead(html.Tr([html.Th("Line"), html.Th("Origin"), html.Th("Season"), html.Th("No. of genes")]))
]

row1 = html.Tr([html.Td("AinaLrFor"), html.Td("Switzerland"), html.Td("Winter"), html.Td("144,075")])
row2 = html.Tr([html.Td("Chinese Sprint"), html.Td("China"), html.Td("Spring"), html.Td("135,155")])
row3 = html.Tr([html.Td("Jagger"), html.Td("USA"), html.Td("Winter"), html.Td("140,579")])
row4 = html.Tr([html.Td("Julius"), html.Td("Germany"), html.Td("Winter"), html.Td("141,170")])
row5 = html.Tr([html.Td("Landmark"), html.Td("Australia"), html.Td("Spring"), html.Td("140,340")])
row6 = html.Tr([html.Td("Lancer"), html.Td("Canada"), html.Td("Spring"), html.Td("140,765")])
row7 = html.Tr([html.Td("Mace"), html.Td("Australia"), html.Td("Spring"), html.Td("140,866")])
row9 = html.Tr([html.Td("Norin61"), html.Td("Japan"), html.Td("Spring"), html.Td("145,506")])
row10 = html.Tr([html.Td("Stanley"), html.Td("Canada"), html.Td("Spring"), html.Td("140,588")])
row8 = html.Tr([html.Td("SyMattis"), html.Td("France"), html.Td("Winter"), html.Td("140,629")])


table_body = [html.Tbody([row1, row2, row3, row4, row5, row6, row7, row9, row10, row8])]

table = dbc.Table(table_header + table_body, bordered=True)


layout = html.Div([
    
    html.Link(
            rel='stylesheet',
            href='../static/stylesheet.css'
        ),

    html.Div(
        id='data', 
        style=
        {
            'width':'100%', 
            'textAlign':'center',
            'padding': '15px',
            'font-size': 'large'
        },children=[
        html.Table(
            style=
            {
                'width':'80%', 
                'textAlign':'left',
                'padding': '15px',
                'position': 'left',
                'left': '10%'
                # 'font-size': 'x-large'
                },
            children=[
            html.Tr(
                children=
                [
                html.Td(
                    children=[
                        "Wheat cultivars used to infer gene families are listed below with number of high-confeice genes used in this analysis.",
                        html.Br(),
                        table,
                        html.Br(),
                        html.Br(),
                        "More information about these cultivars is available from ",
                        html.A("Ensembl Plants", href='https://plants.ensembl.org/Triticum_aestivum/Info/Strains?db=core Ensembl', target='_blank'),
                    ]),
                ]),
            ]),
        ]),


   
    html.Br(),

    
])


if __name__ == '__main__':
    app.run_server(debug=True)