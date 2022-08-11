from dash import Dash, dcc, html, callback, Input, Output

import dash_bootstrap_components as dbc


import requests

import json

import pandas as pd

from apps import config

from .plotly_tree import (
    create_tree,
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

cluster_id = None


def get_homology_table(cluster_id):


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

    r = requests.post(config.grassroots_url,json=ploads)

    if r.status_code == 200:
        response = json.loads(r.text)

        status = response["results"][0]["status"]
        status_text = response["results"][0]["status_text"]




        table_header = [
            html.Thead(html.Tr([html.Th("Gene"), html.Th("Gene"), html.Th("homology")]))
        ]

        homology_row = []
        if status == 5:
            homology = response["results"][0]["results"][0]["data"]["homology"]
            for h in homology.split("},{"):

                # removing quotes ('), { and }, then splitting with comma
                query_id,target_id,homology_type = h.replace("'","").replace("{","").replace("},","").replace("}","").split(",")
                homology_row.append(html.Tr([html.Td(query_id.split(":")[1]),html.Td(target_id.split(":")[1]), html.Td(homology_type.split(":")[1])]))

            table_body = [html.Tbody(homology_row)]

            table = dbc.Table(table_header + table_body, bordered=True)

    return table


if __name__ == '__main__':
    app.run_server(debug=True)

