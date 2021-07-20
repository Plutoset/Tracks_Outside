from windy import *

def init_forecast():
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    fig = make_subplots(
        rows=1, cols=1,
        specs=[
            [{"type": "table"}]
                ]
        )
    fig.add_trace(
        go.Table(
        columnorder = list(range(1,12,1)),
        columnwidth = [100,30,40,40,40,40,40,40,40,40,40],
        header=dict(
            values=[
            '<b>time</b>','',
            '<b>temp</b>', '<b>prec</b>', 
            '<b>RH</b>','<b>wind</b>','<b>aspect</b>','<b>gust</b>',
            '<b>high</b>', '<b>middle</b>', '<b>low</b>'
            ],
            line_color=['white','#D4F2E7','#D4F2E7','#D4F2E7','#D4F2E7','#FFE4C4','#FFE4C4','#FFE4C4','#B0C4DE','#B0C4DE','#B0C4DE'], 
            fill_color=['white','#D4F2E7','#D4F2E7','#D4F2E7','#D4F2E7','#FFE4C4','#FFE4C4','#FFE4C4','#B0C4DE','#B0C4DE','#B0C4DE'],
            align=['right','center','center','center','center','center','center','center','center','center'],
            font=dict(color='black', family='Times New Roman',size=12)
        ),
        cells=dict(
            values=[
            [],[],
                [], [],[], 
                [], [], [], 
                [], [], []
                ],
            align=['right','center','center','center','center','center','center','center','center','center'], 
            font=dict(color='black', family='Times New Roman',size=10)
            )
        ),
        row=1,col=1
    )
    fig.update_layout(
            height=100,
            width=800,
            margin=dict(
                        l=50,
                        r=50,
                        b=20,
                        t=20,
                        pad=4
                         ),
            font = dict(family='Times New Roman'),
            template='simple_white',
            showlegend=False,
            barmode='overlay')
    fig.update_xaxes(tickfont=dict(family='Times New Roman', size=1, color='black'), row=1, col=1,)
    return fig

def set_original(inputlon,inputlat,size):
    import plotly.graph_objects as go
    fig = go.Figure()
    fig = go.Figure(go.Scattermapbox(
                mode = "markers+lines",
                lat=[], lon=[]))
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(mapbox = {
            'center':go.layout.mapbox.Center(
            lat=inputlat,
            lon=inputlon),
            'style': "stamen-terrain",
            'zoom': size})
    return fig

def WGS84_to_WebM(lon,lat):
    #WGS84经纬度坐标转Web墨卡托投影坐标
    import math
    r = 20037508.34
    x = (lon * r) / 180
    y = math.log(math.tan(math.pi/4 + lat * math.pi /360))* r / math.pi
    return x,y

def resize(data,inputX,inputY,outputX,outputY):
    import numpy as np
    scale = (outputX - outputY)/(inputX - inputY)
    datao = (data - inputY) * scale + outputY
    datao = np.round(list(datao))
    datao = np.int32(datao)
    return datao

def speed_colors():
    from plotly.colors import n_colors
    import matplotlib
    d1 = n_colors((1,1,0),(0,1,0), 51)# -80 to 0
    d2 = n_colors((1,0,0),(1,1,0), 50) # 0 to 15
    d = d2+d1
    d = d[::-1]
    d = [matplotlib.colors.rgb2hex(i) for i in d]
    return d

def show_forecast(forecast):
    from plotly.subplots import make_subplots
    from plotly.colors import n_colors
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np
    import math

    def temp():
        from plotly.colors import n_colors
        d1 = n_colors('rgb(102,255,255)','rgb(0,0,153)', 81, colortype='rgb')# -80 to 0
        d2 = n_colors('rgb(51,255,0)','rgb(102,255,255)', 15, colortype='rgb') # 0 to 15
        d3 = n_colors('rgb(255,255,0)','rgb(51,255,0)', 15, colortype='rgb') # 15 to 30
        d4 = n_colors('rgb(255,0,0)','rgb(255,255,0)', 20, colortype='rgb') # 30 to 50
        d = d4+d3+d2+d1
        d = d[::-1]
        return d

    timestr=forecast.time.apply(lambda x: x.strftime('%Hh %d-%m-%Y'))
    temp_colors = temp()
    cloud_colors = n_colors( 'rgb(30,144,255)', 'rgb(240,248,255)', 101, colortype='rgb')

    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.3,0.7],
        shared_xaxes=True,
        vertical_spacing=0.01,
        specs=[
            [{"secondary_y": True}],
            [{"type": "table"}]
                ]
        )
    fig.add_trace(go.Scatter(
                x = forecast.time,
                y = forecast.temp_surface,
                mode = 'lines', 
                name = 'temp(℃)',
                line = dict(color='#F08080'),
            ),row=1,col=1,secondary_y=True)
    fig.add_trace(go.Bar(
                x = forecast.time,
                y = forecast['precipation3h'],
                marker_color = '#1E90FF',
                name = '3h prec(mm)',
            ),row=1,col=1,)
    fig.add_trace(
        go.Table(
        columnorder = list(range(1,12,1)),
        columnwidth = [100,30,40,40,40,40,40,40,40,40,40],
        header=dict(
            values=[
            '<b>time</b>','',
            '<b>temp</b>', '<b>prec</b>', 
            '<b>RH</b>','<b>wind</b>','<b>aspect</b>','<b>gust</b>',
            '<b>high</b>', '<b>middle</b>', '<b>low</b>'
            ],
            line_color=['white','#D4F2E7','#D4F2E7','#D4F2E7','#D4F2E7','#FFE4C4','#FFE4C4','#FFE4C4','#B0C4DE','#B0C4DE','#B0C4DE'], 
            fill_color=['white','#D4F2E7','#D4F2E7','#D4F2E7','#D4F2E7','#FFE4C4','#FFE4C4','#FFE4C4','#B0C4DE','#B0C4DE','#B0C4DE'],
            align=['right','center','center','center','center','center','center','center','center','center'],
            font=dict(color='black', family='Times New Roman',size=12)
        ),
        cells=dict(
            values=[
            timestr,forecast.weather,
                forecast.temp_surface, np.round(list(forecast.precipation3h),decimals=3), 
                forecast.rh_surface, forecast.wind_surface, forecast.wind_aspect, forecast.gust_surface, 
                forecast.hclouds_surface, forecast.mclouds_surface, forecast.lclouds_surface
                ],
            line_color=[
                '#F5F5F5', '#F5F5F5',
                np.array(temp_colors)[np.int32(np.round(forecast.temp_surface))+79],
                '#F5F5F5', '#F5F5F5', '#F5F5F5', '#F5F5F5', '#F5F5F5', 
                np.array(cloud_colors)[forecast.hclouds_surface],
                np.array(cloud_colors)[forecast.mclouds_surface], 
                np.array(cloud_colors)[forecast.lclouds_surface]
                        ],
            fill_color=[
                'white','white',
                np.array(temp_colors)[np.int32(np.round(forecast.temp_surface))+79],
                '#A9A9A9','#A9A9A9', '#A9A9A9', '#A9A9A9','#A9A9A9',
                np.array(cloud_colors)[forecast.hclouds_surface],
                np.array(cloud_colors)[forecast.mclouds_surface], 
                np.array(cloud_colors)[forecast.lclouds_surface]
                        ],
            align=['right','center','center','center','center','center','center','center','center','center'], 
            font=dict(color='black', family='Times New Roman',size=10)
            )
        ),
        row=2,col=1
    )
    fig.update_layout(
            width=800,
            height=450,
            margin=dict(
                        l=50,
                        r=50,
                        b=20,
                        t=20,
                        pad=4
                         ),
            hovermode="x unified",
            yaxis=dict(range=[0, 10**math.ceil(math.log10(max(forecast['precipation3h'][0:20])))]),
            xaxis=dict(gridcolor='black',range=[forecast.time[0], forecast.time[20]]),
            font = dict(family='Times New Roman'),
            template='simple_white',
            showlegend=False,
            xaxis_tickformatstops = [
                dict(dtickrange=[None, 1000], value="%H:%M:%S.%L ms"),
                dict(dtickrange=[1000, 60000], value="%H:%M:%S s"),
                dict(dtickrange=[60000, 3600000], value="%H:%M m"),
                dict(dtickrange=[3600000, 86400000], value="%e %a %Hh"),
                dict(dtickrange=[86400000, 604800000], value="%e (%a)"),
                dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
                dict(dtickrange=["M1", "M12"], value="%b '%y M"),
                dict(dtickrange=["M12", None], value="%Y Y")
            ],
            barmode='overlay')
    fig.update_yaxes(title_text="precipation", row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_text="temperature", row=1, col=1, secondary_y=True)
    fig.update_xaxes(tickfont=dict(family='Times New Roman', size=1, color='black'), row=1, col=1,)
    return fig

def plot_kml(k, originalfig):
    import plotly.graph_objects as go
    import numpy as np
    coordinates = k.get_coordinates()
    fig = originalfig
    
    if k.get_type() == 'raw':  
        newfig=go.Scattermapbox(
            mode = "markers+lines",
            lat=coordinates.lat, lon=coordinates.lon, 
            hovertext=["<b>lon</b>: {lon}<br><b>lat</b>: {lat}<br><b>ele</b>: {ele}".format(lon=a,lat=b,ele=c) for a,b,c in zip(coordinates.lon, coordinates.lat, coordinates.ele)],
            hoverinfo="text",
            name = k.get_author(),
            text = "",
            meta = [coordinates.ele],
            marker = {
                'size': 4,
                })
        fig = fig.add_trace(newfig)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_layout(hoverlabel=dict(
        font_family="Times Now Roman"))
        fig.update_layout(mapbox = {
                'center':go.layout.mapbox.Center(
                lat=coordinates.lat.mean(),
                lon=coordinates.lon.mean()),
                'style': "stamen-terrain",
                'zoom': k.get_tilesize()})
        
    elif k.get_type() == 'detailed':
        newfig = go.Scattermapbox(
            mode = "markers+lines",
            lat=coordinates.lat, lon=coordinates.lon, 
            hovertext=["<b>lon</b>: {lon}<br><b>lat</b>: {lat}<br><b>ele</b>: {ele}<br><b>time</b>: {time}<br><b>speed</b>: {speed}".format(lon=a,lat=b,ele=c,time=h,speed=g) for a,b,c,h,g in zip(coordinates.lon, coordinates.lat, coordinates.ele,coordinates.time,coordinates.speed)],
            hoverinfo="text",
            name=k.get_author(),
            text=coordinates.name,
            marker = {'size': 4,
                    'color': np.array(speed_colors())[k.set_colors()]
                    }
            )
        
        fig = fig.add_trace(newfig)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(hoverlabel=dict(
            font_family="Times Now Roman"))
        fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            legend_title_text='Author',
            ) 
        fig.update_layout(mapbox = {
                'center':go.layout.mapbox.Center(
                lat=coordinates.lat.mean(),
                lon=coordinates.lon.mean()),
                'style': "stamen-terrain",
                'zoom': k.get_tilesize()})
    return fig