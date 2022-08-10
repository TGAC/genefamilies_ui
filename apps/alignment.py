from dash import Dash, dcc, html, callback, Input, Output

import requests

import dash_bio as dashbio

import json

import urllib.request as urlreq

from dash.dash import no_update

from io import StringIO

from apps import config


cluster_id = None


def get_alignments(search):


    ploads = {
        "services": [{
            "so:name": "GeneTrees search service",
            "start_service": True,
            "parameter_set": {
            "level": "simple",
            "parameters": [{
                "param": "GT Cluster",
                "current_value": search
                }]
            }
        }]
    }

    r = requests.post(config.grassroots_url,json=ploads)

    if r.status_code == 200:
        response = json.loads(r.text)

        status = response["results"][0]["status"]
        status_text = response["results"][0]["status_text"]

        sequences = {}
        alignments = {}
        if status == 5:
            tree = response["results"][0]["results"][0]["data"]["genetree"]

            for c in response["results"][0]["results"]:
                alignments[c["data"]["gene_id"]] = c["data"]["alignment"]

    
    fasta = get_fasta(alignments)

    return fasta

def get_fasta(seqs):

    fasta_seq = ""
    for seq in seqs:
        fasta_seq = fasta_seq + ">" + seq + "\n"+ seqs[seq]+"\n"

    return fasta_seq


if __name__ == '__main__':
    app.run_server(debug=True)
