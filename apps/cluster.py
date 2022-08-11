from dash import Dash, dcc, html, callback, Input, Output

import dash_bootstrap_components as dbc

import requests

import json

import dash_bio as dashbio

import urllib.request as urlreq

import pandas as pd

from apps import config


from .plotly_tree import (
    create_tree,
)

from .alignment import (
    get_alignments,
)

from .tree import (
    get_tree,
    get_subtree,
    get_newick_tree
)

from .sequence import (
    get_sequences,
)


from .homology import (
    get_homology_table,
    get_homology_csv
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

cluster_id = None


layout = html.Div([
    
    html.Link(
            rel='stylesheet',
            href='/static/stylesheet.css'
        ),

    html.Table(
        style = {
        'textAlign' : 'center',
        'width':'100%',
        },
        children=[
            html.Tr(
                children=[
                html.Td(
                    style = {
                    'textAlign' : 'right',
                    'width':'50%'
                    },
                    children=[
                        html.Div(style={'padding-top':'10px', 'padding-bottom':'10px'},children=["Showing gene tree with cluster_id :"])
                    ]
                    ),
                html.Td(
                    style = {
                    'textAlign' : 'left',
                    'width':'50%'

                    },
                    children = [
                            html.Div(style={'padding-top':'10px', 'padding-bottom':'10px'}, id="cluster_id", children=[]),
                    ]
                    )])

        ]),

    
    dcc.Tabs(id="tabs-example-graph", value='tab-tree', children=
        [

            dcc.Tab(
                label="Tree",
                value='tab-tree'
            ),
            dcc.Tab(
                label="SubTree",
                value='tab-subtree'
            ),
            dcc.Tab(
                label="Homology",
                value='tab-homology'
            ),
            dcc.Tab(
                label="Alignments",
                value='tab-alignment',
            ),
            dcc.Tab(
                label="Sequences",
                value='tab-sequence'
            ),
            dcc.Tab(
                label="Downloads",
                value='tab-download'
            ),
        ]
    ),
    html.Div(
        id='tabs-content-example-graph',
        style=
                {
                    'width':'100%', 
                    'textAlign':'center',
                    'padding': '15px',
                    'font-size': 'x-large',
                })
    ])

@callback(
    Output('cluster_id', 'children'),
    Input('url', 'search'))
def get_cluster_id(search):

    seq_id = search.replace("?", "")

    global cluster_id

    ploads = {
        "services": [{
            "so:name": "GeneTrees search service",
            "start_service": True,
            "parameter_set": {
            "level": "simple",
            "parameters": [{
                "param": "GT Gene",
                "current_value": seq_id
                }]
            }
        }]
    }

    r = requests.post(config.grassroots_url,json=ploads)

    if r.status_code == 200:
        response = json.loads(r.text)
        status = response["results"][0]["status"]
        status_text = response["results"][0]["status_text"]

        if status == 5:

            cluster_id = response["results"][0]["results"][0]["data"]["cluster_id"]

            return cluster_id


@callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'),
            Input('cluster_id', 'children'),

            )
def render_content(tab, cluster_id):



    if tab == 'tab-tree':


        tree = get_tree(cluster_id)

        return html.Div(
            dcc.Graph(id="genetree", className="div-card", 
                style=
                {
                    'border' : '1px solid black', 
                },
                figure = tree
                )
            )
    elif tab == 'tab-subtree':


        tree = get_subtree(cluster_id)


        return html.Div(
            dcc.Graph(id="subtree", className="div-card", 
                style=
                {
                    'border' : '1px solid black', 
                },
                figure = tree
                )
            )
    elif tab == 'tab-alignment':




        fasta = get_alignments(cluster_id)


        return html.Div(
                id='aln_viewer', 
                style=
                {
                    'width':'100%', 
                    'textAlign':'center',
                    'padding': '15px',
                    'font-size': 'x-large'
                },
                children = [ 
                dashbio.AlignmentChart(id='alignment_viewer2', data=fasta, height=900, tilewidth=30)        # )                
                ]
            ),
    elif tab == 'tab-homology':




        homology = get_homology_table(cluster_id)


        return html.Div(
                id='homology_viewer', 
                style=
                {
                    'width':'100%', 
                    'textAlign':'center',
                    'padding': '15px',
                    'font-size': 'x-large'
                },
                children = [homology
                # dashbio.AlignmentChart(id='alignment_viewer2', data=fasta, height=900, tilewidth=30)        # )                
                ]
            ),
    elif tab == 'tab-sequence':

        viewers = []
        i=0
        sequences = get_sequences(cluster_id)
        for seq in sequences:

            i = i+1
            viewer_id = "sequence_viewer2"+str(i)
            viewers.append(html.Div(className="col",children=[dashbio.SequenceViewer(id=viewer_id, sequence=sequences[seq], title=seq, badge=False)]))

        return html.Div(className="row row-cols-12", children = viewers)

    elif tab == 'tab-download':
        return html.Div(
            children=[
                html.Table(
                style={
                    'width':'100%',
                    'textAlign' : 'left'
                },
                children=[
                    html.Tr(
                        children=[
                        html.Td(
                    children=[
                    "Download Full GeneTree in Newick format"]),
                    html.Td(children=[html.Button("Download Tree", id="btn-download-tree", className="download_btn")]),
                    ]
                    ),
                    html.Tr(
                        children=[
                        html.Td(
                    children=[
                    "Download Sub GeneTree in Newick format"]),
                    html.Td(children=[html.Button("Download Tree", id="btn-download-subtree", className="download_btn")]),
                    ]
                    ),
                    html.Tr(
                        children=[
                        html.Td(
                    children=[
                    "Download Homology"]),
                    html.Td(children=[html.Button("Download Homology", id="btn-download-homology", className="download_btn")]),
                    ]
                    ),
                    html.Tr(
                        children=[    html.Td(
                    children=[
                    "Download Alignment in FASTA format"]),
                    html.Td(children=[html.Button("Download Alignment", id="btn-download-aln", className="download_btn")]),
                    ]
                    ),
                    html.Tr(
                        children=[    html.Td(
                    children=[
                    "Download Sequences in FASTA format"]),
                    html.Td(children=[html.Button("Download Fasta", id="btn-download-fa", className="download_btn")])
                        ]
                    )
                ]),
                dcc.Download(id="download-tree"),
                dcc.Download(id="download-subtree"),
                dcc.Download(id="download-aln"),
                dcc.Download(id="download-fa"),
                dcc.Download(id="download-homology"),
            ])


@callback(
    Output("download-tree", "data"),
    Input("btn-download-tree", "n_clicks"),
    prevent_initial_call=True,
)
def download_tree(n_clicks):

    tree = get_newick_tree(cluster_id, "genetree")
    filename = "GeneTrees_"+cluster_id+"_tree.nhx"

    return dict(content=tree, filename=filename)


@callback(
    Output("download-subtree", "data"),
    Input("btn-download-subtree", "n_clicks"),
    prevent_initial_call=True,
)
def download_subtree(n_clicks):

    tree = get_newick_tree(cluster_id, "subtree")
    filename = "GeneTrees_"+cluster_id+"_tree.nhx"

    return dict(content=tree, filename=filename)


@callback(
    Output("download-aln", "data"),
    Input("btn-download-aln", "n_clicks"),
    prevent_initial_call=True,
)
def download_aln(n_clicks):
    aln_file = get_alignments(cluster_id)
    filename = "GeneTrees_"+cluster_id+"_tree.fa_aln"
    return dict(content=aln_file, filename=filename)


@callback(
    Output("download-fa", "data"),
    Input("btn-download-fa", "n_clicks"),
    prevent_initial_call=True,
)
def download_fa(n_clicks):
    sequences = get_sequences(cluster_id)

    seq_file = ""
    for seq in sequences:
        seq_file = seq_file + "\n>" + seq + "\n"+ sequences[seq]

    filename = "GeneTrees_"+cluster_id+"_tree.fa"
    return dict(content=seq_file, filename=filename)

@callback(
    Output("download-homology", "data"),
    Input("btn-download-homology", "n_clicks"),
    prevent_initial_call=True,
)
def download_homology(n_clicks):
    homology = get_homology_csv(cluster_id)

    filename = "GeneTrees_"+cluster_id+"_homology.csv"
    return dict(content=homology, filename=filename)


if __name__ == '__main__':
    app.run_server(debug=True)


