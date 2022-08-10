import datetime

import dash

import dash_bootstrap_components as dbc

import requests

import json

import pandas as pd

import dash_table_experiments as dt

from dash import dcc, html, Dash, Input, Output, callback, dash_table,  State 

from dash.exceptions import PreventUpdate

from dash.dash import no_update

import dash_defer_js_import as dji

from functools import wraps

from apps import cluster, blast_search, about, data, contact, fetch_blast_results, config

from app import app


sequences = {}
alignments = {}
tree = None

inputs = []
# external JavaScript files
external_scripts = [
    'assets/app.js',
    'https://www.googletagmanager.com/gtag/js?id=G-YG1JGSF1RV',
    'assets/ga.js',
]


external_stylesheets = [
{
    'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
    'rel': 'stylesheet',
    'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
    'crossorigin': 'anonymous'
},
dbc.themes.BOOTSTRAP
]


app = dash.Dash(__name__,
                external_scripts=external_scripts,
                url_base_pathname='/',
                suppress_callback_exceptions=True,
                external_stylesheets=external_stylesheets)


app.title = "GeneTrees Explorer - Wheat"

app._favicon = ("static/images/favicon_1_0.jpg")

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
home = {}
menu = {'Home':"/",'BLAST':"blast_search", 'About':"about", 'Data':'data', 'Contact':"contact"}

app.layout = html.Div(style={
        'display': 'flex',
        'flex-direction': 'column'
    },children = [
    dcc.Location(id='url', refresh=False),
    html.Header(
        style={
        'textAlign':'center'
        },
        id='header', 
        children=[
            html.Table(style={
                    'width':'100%',
                    # 'height':'100px',
                    'background-color':'#2c3e50',
                    'color':'white',
                    'textAlign':'center'
                },children=[
                html.Tr(children=[
                    html.Td(style={
                        'width':'33%',
                        'vertical-align': 'top',
                        'padding': '10px'
                    },children=[
                        html.Div(
                            style={
                            'textAlign':'left'
                            },
                            children=[
                            html.H2(children="Wheat Gene Families"),
                            ]
                            )]),
                    html.Td(style={
                        'width':'33%',
                        'vertical-align': 'top',
                        'padding': '10px',
                        'textAlign':'right'
                    },children=[
                        html.Div(
                            children=[
                                html.Div(
                                    id='menu', 
                                    children=
                                    [
                                        html.A(key, href=menu[key]) for key in menu
                                    ]),
                            ]
                            )])


                        ]
                    )
        ]),
    ]),

    html.Div(id='page-content', style={
          'flex': '1 0 auto',
          'padding':'20px'
        }),
    html.Footer(
            id='footer', 
            children=[
                html.Table(style={
                        'width':'100%',
                        # 'height':'200px',
                        'background-color':'#2c3e50',
                        'color':'white'
                    },children=[

                    html.Tr(children=[
                        html.Td(
                            colSpan=3,
                            style={
                                'width':'33%',
                                'padding':'5px'
                            },
                            children=[
                                "© 2022 - 2022 ", 
                                html.A(" Earlham Institute, UK ", href='http://www.earlham.ac.uk/', target='_blank'), 
                                " Version: 0.0.1 ", 
                                html.A("Feedback", href='mailto:anil.thanki@earlham.ac.uk?Subject=Wheat Gene Families - Feedback')
                            ]) 
                        ])
            ]),
            ]) 
])



def update_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),

    ])

index_layout = html.Div(

    children=[

        html.Link(
            rel='stylesheet',
            href='/assets/static/stylesheet.css'
        ),
       
        html.Div(
            id="index_intro",
            style={
                  'width': '80%',
                  'margin-left': 'auto',
                  'margin-right': 'auto',
                  'padding': '20px',
                  'font-size': 'larger',
                  'color': '#2c3e50'
            },
            children=[
            html.Div(
                children = [
                "This service provides interface to search for gene families derived from the wheat cultivars. More information about the dataset, infrastructure and service is available",
                html.A(" here.", href='about', target='_blank'),
                html.Br(),
                html.Br(),
                "More information on dataset used for this analysis is available ",
                html.A(" here.", href='data', target='_blank'),
                html.Br(),  
                html.Br(),
                "Gene families can be searched by sequence of interest using our ",
                html.A("BLAST", href='blast_search', target='_blank'),
                " search functionality." ,
                "Previously queried results can also be retrived from our ",
                html.A("fetch BLAST", href='fetch_blast_results', target='_blank'),
                " functionality."
                ])
            ]),
                html.Div(
            id='footer_above', 
            style={
                'left':'-0px',
                'width':'100%'
            },
            children=[
                html.Table(style={
                        'width':'100%',
                        'height':'200px',
                        'background-color':'#2c3e50',
                        'color':'white'
                    },children=[
                     html.Tr(children=[
                        html.Td(),
                        html.Td(
                        # colSpan = 3,
                        style={
                        'width':'33%',
                        'vertical-align': 'top',
                        'padding': '20px'
                    },children=[
                            html.Div(id='funders-logo',
                                style={
                                'textAlign':'center',
                                'width':'100%'
                                },
                                children=[
                                html.H3("Funders"), 
                                html.Table(
                                    style={
                                },
                                    children=[
                                    html.Tr(
                                        children=[
                                        html.Td(
                                            children=[
                                
                                html.A(html.Img(src=app.get_asset_url('../assets/static/images/DFW-logo-white.png'), style={'height':'50px'}),
                                href='https://designingfuturewheat.org.uk/', target='_blank'),
                                html.Br(),
                                html.A("Designing Future Wheat", href='https://designingfuturewheat.org.uk/', target='_blank'),
                                            ]
                                            ),
                                        html.Td(
                                html.A(html.Img(src=app.get_asset_url('../assets/static/images/EI-double-whiteout-trans.png'), style={'height':'50px'}),
                                             href='https://www.earlham.ac.uk', target='_blank')),
                                        html.Td(
                                html.A(html.Img(src=app.get_asset_url('../assets/static/images/funder-logo-bbsrc.png'), style={'height':'75px'}),
                                href='https://bbsrc.ukri.org/', target='_blank'),
                                            )])])
                                ])]),
                        html.Td(),
                    
                    ])
            ]),
            ]) 
    ]

)


not_found_layout = html.Div(

    children=[

        html.Link(
            rel='stylesheet',
            href='/assets/static/stylesheet.css'
        ),
       
        html.Div(style={
            'width':'100%',
            'textAlign':'center'
            },children=
        [
            html.H2("404: Not found", className="text-danger"),
            html.Hr(className="my-2"),
            html.P(children=[
                "The page you are looking for is not recognised. Please go back to "
                ,
            html.A("Homepage", href='/')]),
            
        ],
        className="h-100 p-5 bg-light border rounded-3",
    )
    ]

)


@callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index_layout
    elif pathname == '/blast_search':
        return blast_search.layout
    elif pathname == '/cluster':
        return cluster.layout
    elif pathname == '/about':
        return about.layout
    elif pathname == '/data':
        return data.layout
    elif pathname == '/contact':
        return contact.layout
    elif pathname == "/fetch_blast_results":
        return fetch_blast_results.layout
    else:
        return not_found_layout
        
if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
