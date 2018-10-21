from flask import Flask
from dash import Dash
import daru
import json
import operator
import dash
import dash_html_components as html
import dash_core_components as dcc

server = Flask(__name__)
app = Dash(__name__, server=server, url_base_pathname='/')

app.layout = html.Div(
    children=[html.Button('Submit', id='button')]
)

def json_response(json_string):
    response = server.response_class(
        response=json_string,
        status=200,
        mimetype='application/json'
    )

    return response

@server.route("/api/patches/")
def patches():

    num_patches = 200

    indices = daru.read_index("daru.idaru")
    metric_sorted = sorted(indices.items(), key=operator.itemgetter(1), reverse=True)
    top_indices = metric_sorted[:num_patches:]

    to_json = dict(top_indices)

    json_string = json.dumps(to_json)

    return json_response(json_string)

def records_to_json(records):
    record_dicts = []
    for record in records:
        record_dict = {
        "day"  : record.day,
        "qname": record.qname,
        "flags": record.flags,
        "rname": record.rname,
        "pos"  : record.pos,
        "mapq" : record.mapq,
        "cigar": record.cigar,
        "seq"  : record.seq,
        "qual" : record.qual
        }
        record_dicts.append(record_dict)

    json_string = json.dumps(record_dicts)

    return json_response(json_string)

if __name__ == "__main__":
    server.run()
