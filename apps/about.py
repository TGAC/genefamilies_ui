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
                # 'font-size': 'x-large'
                },
            children=[
            html.Tr(
                children=
                [
                html.Td(
                    children=[
                    html.Div("This service provides an interface to search for gene families derived from wheat cultivars. Gene Families were identified using the GeneSeqToFamily pipeline."),
                    html.Br(),
                    html.Div("For this analysis gene annotations were generated at Earlham Institute, UK in collboration with Helmholtz Zentrum München: German Research Center for Environmental Health (project code here)"),
                    html.Br(),


                    ])
                ]
                ),
                html.Tr(
                    children=[
                    html.Td(
                        children=[
                        html.H4("GeneSeqToFamily"),
                        html.Br(),
                        html.Div("Gene Families are identified using the GeneSeqToFamily pipeline."),
                        html.Br(),
                        html.Div("GeneSeqToFamily is a comprehensive workflow to identify gene families from a set of sequences. The workflow is designed to work within the Galaxy environment as well as on the command line with the Snakemake workflow management system."),
                        html.Br(),
                        ]
                    )]
                ),
                html.Tr(
                    children=[
                    html.Td(
                        children=
                        [
                        html.H4("CyVerseUK and Grassroots"),
                        html.Div("This service is hosted on CyVerseUK infrastructure and BLAST service is provided by The Grassroots Infrastructure project."),
                        html.Br(),

                        ]
                    )]
                ),
                html.Tr(
                    children=[
                    html.Td(
                        children=
                        [
                        html.H4("Designing Future Wheat"),
                        
                        html.Div("This project is strategically funded through the BBSRC Designing Future Wheat programme grant, BB/P016855/1, and aims to develop a lightweight reusable set of open-source software tools to allow researchers to share and federate life science datasets."),
                        html.Br(),

                        html.Div("The BBSRC funded Designing Future Wheat Institute Strategic Programme (ISP), spans eight research institutes and universities and aims to develop new wheat germplasm containing the next generation of key traits. Building on this research we will then provide this new germplasm in a readily accessible and referenced form to commercial crop breeders and the plant science community."),
                        html.Br(),


                        html.Div("The cross-institute programme grant, Designing Future Wheat (DFW), is the first flagship project of its kind to bring the UK’s wheat researchers together to deliver new varieties relevant to the international stage, through the coordinated effort of biologists, breeders, and informaticians. As such, Grassroots is funded by the DFW programme, enabling us to build a platform that can meet the needs of not only this ambitious programme but the wider UK and international wheat community that needs fast and openly-licenced unfettered access to the data and experimental information arising from DFW."),
                        html.Br(),

                        ]
                    )]
                ),
                html.Tr(
                    children=[
                    html.Td(
                        children=
                        [
                        html.H4("Citation"),
                        html.Div("If you have used any of the data from this service in your research, we would very much appreciate it if you let us know and cite us in any publications, as follows:"),
                        html.Br(),
                        html.Div("Thanki AS, Soranzo N, Haerty W, Davey RP. GeneSeqToFamily: a Galaxy workflow to find gene families based on the Ensembl Compara GeneTrees pipeline. Gigascience. 2018 Mar 1;7(3):1-10. doi: 10.1093/gigascience/giy005. PMID: 29425291; PMCID: PMC5863215."),
                        ]
                        )
                    ]
                    ),


            ])
        ]
    ),


   
    html.Br(),

])


if __name__ == '__main__':
    app.run_server(debug=True)