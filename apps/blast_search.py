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

from apps import sequence, alignment, tree, cluster, config

inputs = []


table_header = [
    html.Thead(html.Tr([html.Th("BLAST ID"), html.Th("Run Status"), html.Th("Last checked")]))
]

row1 = html.Tr([html.Td(children=[html.Div(id='blast-run'), html.Div(id='blast-run-share')]), html.Td(html.Div(id='blast-run-state2')), html.Td(html.Div(id='check-time'))])

table_body = [html.Tbody([row1])]



layout = html.Div(

    children=[

        html.Link(
            rel='stylesheet',
            href='/static/stylesheet.css'
        ),

        html.H3(
            children="BLAST search",
        ),

        dcc.Textarea(
            id='blast-seq', 
            placeholder='Enter a protein sequence...', 
            style={
            'width': '100%', 
            'height': 300, 
            'font-size': 'large',
            'color': 'dimgray'
            }),

        html.Br(),

        html.Table(
            html.Tr(children=[
                html.Td(
            html.Button(style={
            'padding': '5px',
            'font-size': 'large',
            },
            children='Submit BLAST', 
            id='submit-val', 
            n_clicks=0, 
            )),
        html.Td(
            html.Button(style={
            'padding': '5px',
            'font-size': 'large',
            },
            children='Example BLAST Run', 
            id='example-val', 
            n_clicks=0, 
            )),
            ])
        ),

        dcc.Interval(id='interval1', interval=5 * 1000, n_intervals=0, disabled=True),

        html.H1(id='label1', children='',
            style={
            'textAlign': 'right',
            'display' : 'none'
        }),

        html.Hr(),

        dbc.Table(table_header + table_body, bordered=True, style={'width': '100%', 'textAlign' : 'center'}, id="metainfo"),

        html.Div(children=[
            "State", 
            html.Div(id='blast-run-state'), 
            "StateId", 
            html.Div(id='blast-run-state-id'),
            ],
            style={
            'textAlign': 'right',
            'display' : 'none'
        }),

        html.Hr(),

        html.Div(
            id='blast-result',
            # data=''
        ),

        html.Div(id='blast-result2'), 

        html.Div(id='sequence_box'), 
        
    ]

)


@callback(
    Output('label1', 'children'),
    Input('interval1', 'n_intervals')
)
def update_interval(n):
    if n == 0:
        raise PreventUpdate
    else:
        return 'Intervals Passed: ' + str(n)


@callback(
    Output('submit-val', 'n_clicks'),
    Output('blast-seq', 'value'),
    Input('example-val', 'n_clicks'),
)
def example_blast(n_clicks):
    if n_clicks == 0:
        raise PreventUpdate
    else:
        return 1, "MEPTEDIEFLWKWRKYLLLLATLVASVTYGVGLNPPGGVWSQDQEGGTSNAREHRGGAVQPPAPPLLPPAPAPAVYPNRVGDPVLVSTYMRRYTAFFYCNAAAFVASLVIIMFLLDRRISGNRVGLTVLRSAMLLDLLALMAAFAAGSCRDVVASIYVSALFAVVFVYVALHVGVASASSGSSLLLLLGRKAPDSCPWDAEENKYIRERRKFLFLLATFATSLTYAAGLAPPGGFWTKTVAGHRAGAPLLHDGRYKIRYHAFFYANATSFVASLAIIMLLMSRTLRDRLARSYALLVCVLVELLGLMAAYAAGSCRWPTTTVYVFSLVGAVLLYILLQMAIAVFAMDKFKKWREAICNIVTTCAGKSGPKQEIVKQKRDKKTNFDNGPEDKVEASRSLVLLLATLAATVTYQAGLSPPGGVWPEDDDQGRTHHVPGNPVLHDMHSKRYKAFYHCNTAAFVASVVVIIIVQSKQLSAVGRAALKTAMILDLFSLMGAYVAGSCRDRITTVYVAALAVAVFVYSIAKVVAFTAQGRQTMPIECMKRLSGRLSRFLKLSSDETPRPGGAEPATQGLPAVDAGHHPDEPSSQGGEDTPQVHGPASLLTDDLSSIQETQPGSASEGKHTLEENLENKHVILEKKSLERKRKFLLQLAILAATVTYQTGLNPPGGFWTESNGVRKVTAGDPILLDYYGVRYQVFFYCNATGFMASVAVILLLVNQTLSKQGIRSNALHVCVMIGLLGLMGAYATGSCRKLRTSIYVFALVAAVIAFLILEILFYVYADRRNLSEHPWVPQCLQRLLKPLSSAPMGPDDENDKDKVSASKRLQQKRRRVKYEKRKSLMLLGILAASVTYQAGLAPPGGTWGDDDNASSPSPSPSPSSLSPSPSAAYISVAGNPILLNTNAERYQAFFYCNATSFVASVVVIMLVLLRTVKKKRGAPLWAMQTAVVLDLLGLLGAYAAGSCRDWETSGYVIALVAVVVVFITIYVLLSFDAVLGKAKQLTVWKYFSDKKEKLLKYLGRSNDPPGWPVPVTRV"
    



@callback(
    Output('blast-run', 'children'),
    Output('interval1', 'n_intervals'),
    Output('blast-run-share', 'children'),
    Input('submit-val', 'n_clicks'),
    State('blast-seq', 'value')
)
def submit_blast(n_clicks, value):
    if value is None:
        raise PreventUpdate
    else:
        ploads = {
            "services": [{
            "start_service": True,
                "so:name": "BlastP",
                "parameter_set": {
                    "level": "simple",
                    "parameters": [{
                        "param": "query",
                        "current_value": value}, {           
                        "param": config.grassroots_db,
                        "current_value": True,
                        "group": "Available Databases provided by EI Grassroots Dev"
                    }, {
                        "param": "task",
                        "current_value": "blastp"
                    }, {
                        "param": "outfmt",
                        "current_value": 7
                    }
                    ]
                }
            }]
        }
    r = requests.post(config.grassroots_url,json=ploads)
    # change if for failed/empty job submission
    if r.status_code == 200:

        response = json.loads(r.text)

        status = response["results"][0]["status_text"]
        status_id = response["results"][0]["status"]
        jobid = response["results"][0]["job_uuid"]
        
        share_link = "fetch_blast_results?"+jobid
        return jobid, 1, html.A(html.I(className="fas fa-share-alt"), href=share_link, target="_blank")
    else:
        return jobid, 'Err: "{}"'.format(
        r.status_code
    )


@callback(
    Output('blast-run-state2', 'children'),
    Output('blast-run-state-id', 'children'),
    Output("interval1", "disabled"),
    Output("check-time", "children"),
    Input('blast-run-state-id', 'children'),
    Input('blast-run', 'children'),
    Input('interval1', 'n_intervals')
)
def check_run(state, jobid, n_intervals):

    if jobid is None:
        raise PreventUpdate
    else:
        # time.sleep(5)


        ploads = {
            "operations": {
            "operation" : "get_service_results"},
            "services" : [jobid]
            }

        r = requests.post(config.grassroots_url,json=ploads)

        if r.status_code == 200:

            response = json.loads(r.text)

            if response[0]:

                status = response[0]["status"]
                status_text = response[0]["status_text"]


                if status == -3:
                    return "Failed", no_update, False, str(datetime.datetime.now().strftime("%H:%M:%S"))
                elif status ==-2:
                    return "Failed to Start", no_update, False, str(datetime.datetime.now().strftime("%H:%M:%S"))
                elif status == -1:
                    return "Error", no_update, False, str(datetime.datetime.now().strftime("%H:%M:%S"))
                elif status == 0:
                    return "Idle", status, False, str(datetime.datetime.now().strftime("%H:%M:%S"))
                elif status == 1:
                    return "Pending", status, False, str(datetime.datetime.now().strftime("%H:%M:%S"))
                elif status == 2:
                    return "Started", status, False, str(datetime.datetime.now().strftime("%H:%M:%S"))
                elif status == 3:
                    return "Finished unsuccessfully", status, False, str(datetime.datetime.now().strftime("%H:%M:%S"))
                elif status == 4:
                    return "Partially Succeeded", status, False, str(datetime.datetime.now().strftime("%H:%M:%S"))
                elif status == 5:
                    return "Succeeded", status, True, str(datetime.datetime.now().strftime("%H:%M:%S"))
                elif status == 6:

                    return "Cleaned up", status, True, str(datetime.datetime.now().strftime("%H:%M:%S"))


@callback(
    Output('blast-result', 'children'),
    Input('blast-run-state-id', 'children'),
    State('blast-run', 'children'),
)

def get_results(state, jobid):

    if jobid is None:
        raise PreventUpdate
    else:

        ploads = {
            "operations": {
            "operation" : "get_service_results"},
            "services" : [jobid]
            }

        r = requests.post(config.grassroots_url,json=ploads)

        if r.status_code == 200:

            response = json.loads(r.text)

            if response[0]:

                status = response[0]["status"]
                status_text = response[0]["status_text"]

                if status in [-3, -2, -1, 0, 1, 2, 3]:
                    return ""
                elif status in [4, 5]:
                    
                    df = pd.DataFrame([x.split('\t') for x in response[0]["results"][0]["data"].split('\n') if "#" not in x])

                    test = [x.split(',') for x in response[0]["results"][0]["data"].split('\n') if "Fields" in x]

                    df.columns = test

                    return generate_table(df)
                else:
                    return no_update

def generate_table(dataframe, max_rows=100):
    for i in range(min(len(dataframe), max_rows)):
        inputs.append(Input(dataframe.iloc[i][1], "n_clicks"))


    return html.Table(className="sortable BLAST_results",
                      children=[
        html.Thead(
            html.Tr( children=[html.Th(col) for col in dataframe.columns] + [
                # html.Th("Tree"),
                # html.Th("Sequence"),
                # html.Th("Alignment"),
                html.Th("GeneTree"),
                ])
        ),
        html.Tbody([
            html.Tr(children=[
                # replaceing ariana with arina as misspelled in first run
                html.Td(dataframe.iloc[i][col].replace("ariana", "arina")) for col in dataframe.columns] + [
                html.Td(dcc.Link('Fetch GeneTree', target='_blank', href='cluster?' + dataframe.iloc[i][1].replace("ariana", "arina").replace("_1", ""))),
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


if __name__ == "__main__":
    app.run_server(debug=True, port=8051)

