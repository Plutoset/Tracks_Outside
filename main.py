from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import base64
import dash
import json
import io
from kml import kml
from windy import *
from paint import *
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

init_map = set_original(121,30,8)
init_map.update_layout(clickmode='event+select')

app.layout = html.Div([
     html.H1(
        children='Tracks outside',
        style={
            'textAlign': 'center',
            'color': "#191970",            
            'background-color': "#F0F8FF"
        }
    ),
    html.Div([html.H6(
        children = 'Wanna checkout the conditions of the destination you are longing to?',
        style = {
            'textAlign': 'center',
            'color': "#191970"
        }
    )],style={
        'display': 'flex',
            'textAlign': 'center',
            'justify-content': 'center',
            'flex-direction': 'row'
    }
    ),
    html.Div([html.H6(
        children = 'Here we try to visualize kml tracks ,especially those produced by 2bulu (which do not strictly follow the standards), and see whether the weather condition is nice to go for a trip or not.',
        style = {
            'textAlign': 'center',
            'color': "#191970",

        }
    )],style={
        'display': 'flex',
            'textAlign': 'center',
            'justify-content': 'center',
            'flex-direction': 'row'
    }
    ),
    dcc.Store(id='nowkml'),
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '50%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                "display": "inline-block",
                'textAlign': 'center',
                'margin-left':'25%',
                'margin-buttom':'40px' ,             
            'justify-content': 'center'
            },
        # multiple=True # Allow multiple files to be uploaded
    ),]),
    html.Div(id='output-data-upload',
            children='Infomation',
            style={
                'width': '60%',
                'borderRadius': '5px',
                'color': "#191970",
                'background-color': "#F0F8FF",
                "display": "flex",
                'textAlign': 'center',
                'margin-left':'20%',
                'margin-buttom':'20px' , 
                'margin-top':'20px',            
            'justify-content': 'center'
            },),
    # html.Div([html.Button("Download As Shapefiles", id="btn_txt"), dcc.Download(id="download-text")]),
    html.Div([dcc.Graph(
        id = 'kml-map',
        figure = init_map,style={
            'margin-top':'40px' ,
        }
            )]),
   
        html.Div([html.H6(
            id='location-clicked',
            children='Choose a location to see the weather forecast here',)],
            style={
            'display': 'flex',
            'textAlign': 'center',
            'justify-content': 'center',
            'color': "#191970",
            }), 
        html.Div([
            html.Button('Checkout Weather', id='weather-check', n_clicks=0,
        style={
            'display': 'flex',
            'textAlign': 'center',
            'justify-content': 'center',
            'color': "#191970"
        }),
        ],style={
            'display': 'flex',
            'textAlign': 'center',
            'justify-content': 'center'
        }),
    html.Div([
        html.Div([
            dcc.Graph(
                id = "weather-forecast",
                figure = init_forecast(),
                style={
                        'width':'80%',
                        "display": "flex",
                        'justify-content': 'center',
                          },
            )
        ],style={
            'display': 'flex',
            'textAlign': 'center',
            'justify-content': 'center',
        })
    ],style={
            'display': 'flex',
            'textAlign': 'center',
            'justify-content': 'center',
        }),
    dcc.Markdown(
        '''
        This is a final project for Software Engineering and GIS Development produced by Tangbo@https://github.com/Plutoset.
        '''
    ),
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),

    # dcc.Link('Navigate to "/"', href='/'),
])

@app.callback(
    Output('location-clicked', 'children'),
    Input('kml-map', 'clickData'))
def display_click_data(clickData):
    clickjson = json.loads(json.dumps(clickData, indent=2))
    try:
        clicklon = clickjson['points'][0]['lon']
        clicklat = clickjson['points'][0]['lat']
        outputData = dict()
        outputData['lon'] = clicklon
        outputData['lat'] = clicklat
        return u'longitude: {}, latitude: {}'.format(clicklon, clicklat)
    except:
        return 'Choose a location to see the weather forecast here'

@app.callback(
    Output('weather-forecast', 'figure'),
    [Input('weather-check','n_clicks')],
    state=[State('location-clicked', 'children')]
        )
def nowpoint_forecast(nclicks,location):
    try:
        locations = json.dumps(location)
        locations = locations.split(sep='\n')
        locations = ''.join(locations)
        locations = locations.replace('\n','')
        locations = locations.replace(' ','')
        locations = locations.replace('"','')
        locations = locations.replace("'","")
        locations = locations.replace('longitude:','')
        locations = locations.replace('latitude:','')
        locations = locations.replace('\n','')
        (lon,lat) = locations.split(sep=',')
        lon = float(lon)
        lat = float(lat)
        # forecast1 = forecast_all(lon,lat)
        import joblib
        forecast1 = joblib.load('https://github.com/Plutoset/Tracks_Outside/blob/master/forecast.pkl?raw=true')
        return forecast1
    except:
        return init_forecast()

def parse_contents(contents, filename, originalFig):
    content_type, content_string = contents.split(',')
    Fig = go.Figure(data=originalFig['data'],layout=originalFig['layout'])
    decoded = base64.b64decode(content_string)
    try:
        if '.kml' in filename:
            show_kml = kml(
                io.StringIO(decoded.decode('utf-8'))
                )
            header = show_kml.get_header()
            header = header.split(sep='<br>')
            marker = []
            for dd in header:
                if dd != '':
                    marker.append(dd)
            markers = [dcc.Markdown(i)for i in marker]
            return html.Div(
                markers
            ),show_kml.get_json(),plot_kml(show_kml,Fig)
        else:
            return html.Div([
            'Unmatching file type detected.'
        ]),'',Fig

    
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ]),'',Fig
    

@app.callback(Output('output-data-upload', 'children'),
                Output('nowkml','data'),
                Output('kml-map','figure'),
                Input('kml-map','figure'),
                Input('upload-data', 'contents'),
                State('upload-data', 'filename'),
                )
def update_output(originalFig, list_of_contents, list_of_names):
    if list_of_contents is not None:
        return parse_contents(list_of_contents, list_of_names, originalFig)
    else:
        return (None,'',originalFig)

from flask import request
server = app.server

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    sys.exit("Bye!")

# 没想好，说不定就放弃了
# @app.callback(
#     Output("download-text", "data"),
#     Input("nowkml","data"),
#     Input("btn_txt", "n_clicks"),
#     prevent_initial_call=True,
# )
# def download(kmldata, n_clicks):
#     if kmldata != '':
#         kmlio = io.StringIO()
#         kmlio.write(kmldata)
#         download_kml = kml(kmlio)
#         return dict(content="Hello world!", filename="hello.txt")



if __name__ == '__main__':

    app.run_server(debug=True, port = 8090, use_reloader=False, dev_tools_hot_reload =True, threaded=True)
    sys.exit("Bye!")