from flask import Flask
from dash import Dash

import dash
import dash_html_components as html
import dash_core_components as dcc


server = Flask(__name__)
app = Dash(__name__, server=server, url_base_pathname='/')

app.layout = html.Div(
    children=[html.Button('Submit', id='button')]
)

@server.route("/api/")
def root():
    return "{ token: \"43489238947238732\" }"

if __name__ == "__main__":
    server.run()
