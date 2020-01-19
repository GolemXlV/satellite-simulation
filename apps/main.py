import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from pathlib import Path

from app import app

if 'DYNO' in os.environ:
    app_name = os.environ['DASH_APP_NAME']
else:
    app_name = 'satellite-prediction'

df = pd.read_csv(Path('apps/data/train.csv'), index_col=['id'])

layout = html.Div([
    html.Div([html.H1("Real Satellite position")],
             style={'textAlign': "center", "padding-bottom": "10", "padding-top": "10"}),
    html.Div(
        [html.Div(dcc.Dropdown(id="select-satellite", options=[{'label': 'Satellite #%s' % i, 'value': i}
                                                               for i in df.sat_id.value_counts().index.sort_values()],
                               value=[0], multi=True), className="first-column",
                  style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "33%"}),
         ], className="row", style={"padding": 14, "display": "block", "margin-left": "auto",
                                    "margin-right": "auto", "width": "80%"}),
    html.Div([dcc.Graph(id="my-graph")])
], className="container")


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("select-satellite", "value")]
)
def ugdate_figure(selected_satellites):
    udf = df[df.sat_id.isin(selected_satellites)]
    trace = [go.Scatter3d(
        x=udf[udf.sat_id == i].x, y=udf[udf.sat_id == i].y, z=udf[udf.sat_id == i].z,
        mode='markers', marker={'size': 8, 'colorscale': 'Blackbody', 'opacity': 0.8 })
        for i in udf.sat_id.value_counts().index.sort_values()]
    return {"data": trace,
            "layout": go.Layout(
                height=700, title=f"Satellites <br>{selected_satellites}",
                paper_bgcolor="#f3f3f3",
                scene={"aspectmode": "cube", })
            }
