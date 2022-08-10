from dash import Dash, dcc, html, callback, Input, Output

import requests

import json

import pandas as pd

from .plotly_tree import (
    create_tree,
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

cluster_id = None

def get_tree(cluster_id):


    global tree
    
    tree = get_newick_tree(cluster_id, "genetree")
    
    return create_tree(tree)

def get_subtree(cluster_id):


    global tree
    
    tree = get_newick_tree(cluster_id, "subtree")
    
    return create_tree(tree)

def get_newick_tree(cluster_id, treetype):


    global tree
    ploads = {
        "services": [{
            "so:name": "GeneTrees search service",
            "start_service": True,
            "parameter_set": {
            "level": "simple",
            "parameters": [{
                "param": "GT Cluster",
                "current_value": cluster_id
                }]
            }
        }]
    }

    r = requests.post('https://grassroots.tools/dev/grassroots/public_backend',json=ploads)

    if r.status_code == 200:
        response = json.loads(r.text)

        status = response["results"][0]["status"]
        status_text = response["results"][0]["status_text"]


        if status == 5:
            tree = response["results"][0]["results"][0]["data"][treetype]
    
    return tree


if __name__ == '__main__':
    app.run_server(debug=True)

