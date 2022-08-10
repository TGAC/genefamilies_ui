from dash import Dash, dcc, html, callback, Input, Output

import requests

import json

import pandas as pd

from .plotly_tree import (
    create_tree,
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


layout = html.Div([
    
    html.Link(
            rel='stylesheet',
            href='../static/stylesheet.css'
        ),

    html.Div(
        id='about', 
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
                },
            children=[
                html.Tr(
                    children=[
                    html.Td(
                        children=[
                        html.H4("Contact Us"),
                        html.Div(
                            children=[
                                "If you have any queries, please let us know ",
                            ])
                        ]
                        )]
                    )]),
        html.Br(),
        html.Table(
            style=
            {
                'width':'100%', 
                'textAlign':'center',
                'padding': '15px',
                'position': 'left',
                'left': '10%',
                'vertical-align': 'top',
                # 'font-size': 'x-large'
                },
            children=[
                html.Tr(
                    children=[
                    html.Td(style=
                    {
                        'width':'20%', 
                        'vertical-align': 'top',
                        },
                        children=
                        [
                            html.H4("Anil Thanki"),
                            html.H6("Postdoctoral Research Scientist in Haerty Group"),
                            dcc.Link('Anil.Thanki@earlham.ac.uk', target='_blank', href='mailto:Anil.Thanki@earlham.ac.uk')
                        ]
                        ),
                        html.Td(
                            style=
                    {
                        'width':'20%', 
                        'vertical-align': 'top',
                        },
                        children=
                        [
                            html.H4("Wilfried Haerty"),
                            html.H6("Group Leader"),
                            dcc.Link('Wilfried.Haerty@earlham.ac.uk', target='_blank', href='mailto:Wilfried.Haerty@earlham.ac.uk')

                        ]
                        ),
                        html.Td(
                            style=
                    {
                        'width':'20%', 
                        'vertical-align': 'top',
                        },
                        children=
                        [
                            html.H4("Robert Davey"),
                            html.H6("Head of e-infrastructure"),
                            dcc.Link('Robert.Davey@earlham.ac.uk', target='_blank', href='mailto:Robert.Davey@earlham.ac.uk')
                        ]
                        ),
                        html.Td(
                            style=
                    {
                        'width':'20%', 
                        'vertical-align': 'top',
                        },
                        children=
                        [
                            html.H4("Nicola Soranzo"),
                            html.H6("Galaxy Platform Development Officer"),
                            dcc.Link('Nicola.Soranzo@earlham.ac.uk', target='_blank', href='mailto:Nicola.Soranzo@earlham.ac.uk')
                        ]
                        ),
                        html.Td(
                            style=
                    {
                        'width':'20%', 
                        'vertical-align': 'top',
                        },
                        children=
                        [
                            html.H4("Simon Tyrell"),
                            html.H6("Wheat Initiative Software Engineer"),
                            dcc.Link('Simon.Tyrell@earlham.ac.uk', target='_blank', href='mailto:Simon.Tyrell@earlham.ac.uk')
                        ]
                        ),
                    ]
                    ),
            ])
        ]
    ),
   
    html.Br(),

])


if __name__ == '__main__':
    app.run_server(debug=True)
