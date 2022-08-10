from dash import Dash, dcc, html, callback, Input, Output

import requests

import dash_bio as dashbio

import json

import urllib.request as urlreq

from dash.dash import no_update

from io import StringIO

from dash_bio.utils import protein_reader

cluster_id = None


def get_sequences(cluster_id):


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


        sequences = {}
        if status == 5:
            tree = response["results"][0]["results"][0]["data"]["genetree"]

            for c in response["results"][0]["results"]:

                sequences[c["data"]["gene_id"]] = c["data"]["sequence"]

            
    viewers = []
    i = 0
    for seq in sequences:
        i = i+1
        viewer_id = "sequence_viewer2"+str(i)
        viewers.append(html.Div(className="col",children=[dashbio.SequenceViewer(id=viewer_id, sequence=sequences[seq], title=seq, badge=False)]))

    return sequences 

if __name__ == '__main__':
    app.run_server(debug=True)
