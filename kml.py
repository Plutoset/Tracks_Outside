import time

class kml():
    def __init__(self, Input):
        from io import StringIO
        import xmltodict, json
        if isinstance(Input, str):
            with open(Input,'rb') as kml:
                obj = xmltodict.parse(kml.read())
        elif isinstance(Input,StringIO):
            kml = Input.getvalue()
            obj = xmltodict.parse(kml)
        obj = json.loads(json.dumps(obj))
        self.JSON = obj
        self.set_coordinates()
        self.set_info()
        self.calculate_range()

    def set_coordinates(self):
        import numpy as np
        import pandas as pd
        obj = self.JSON
        folder = obj['kml']['Document']['Folder']
        try:
            datafolder = folder[1]
        except:
            datafolder = folder

        if 'LineString' in datafolder['Placemark'].keys():
            coordinates = datafolder['Placemark']['LineString']['coordinates']
            coordinates = coordinates.split(sep=' ')
            coordinates = [i.split(sep=',')for i in coordinates]
            coordinates = np.array(coordinates)
            coordinates = pd.DataFrame(data=coordinates,columns=['lon','lat','ele'])
            coordinates.lon = [float(i) for i in list(coordinates.lon)]
            coordinates.lat = [float(i) for i in list(coordinates.lat)]
            coordinates.ele = [float(i) for i in list(coordinates.ele)]
            self.coordinates = coordinates
            self.type =  'raw'
        else:
            gxTrack = datafolder['Placemark']['gx:Track']
            gxCoord = gxTrack['gx:coord']
            gxWhen = gxTrack['when']
            gxExtendedData = gxTrack['ExtendedData']
            coordinates = gxCoord
            coordinates = [i.split(sep=' ')for i in coordinates]
            coordinates = np.array(coordinates)
            coordinates = pd.DataFrame(data=coordinates,columns=['lon','lat','ele'])
            coordinates['time'] = list(pd.to_datetime(gxWhen))
            d = gxExtendedData['Data']['value']
            d = [i.split(',') for i in d.split(';')]
            d = pd.DataFrame(d)
            speed = d[0]
            speed = list(speed)
            speed = speed[:-1]
            speed = [float(i) for i in speed]
            coordinates['speed'] = speed
            coordinates.lon = [float(i) for i in list(coordinates.lon)]
            coordinates.lat = [float(i) for i in list(coordinates.lat)]
            coordinates.ele = [float(i) for i in list(coordinates.ele)]
            self.type = 'detailed'
            coordinates['name'] = ''
            try:
                markers = obj['kml']['Document']['Folder'][0]['Placemark']
                for marker in markers:
                    markedTime = marker['TimeStamp']['when']
                    markedPoint = marker['Point']['coordinates']
                    markedPoint = markedPoint.split(sep=',')
                    markedPoint = [float(i) for i in markedPoint]
                    markedName = marker['name']
                    markedTime = pd.to_datetime(markedTime)
                    if coordinates[
                        (coordinates.lat == markedPoint[1]) & 
                        (coordinates.lon == markedPoint[0]) & 
                        (coordinates.ele == markedPoint[2])
                        ].shape[0] == 0:
                        markerWrite = [{'lon':markedPoint[0],
                                                    'lat':markedPoint[1],
                                                    'ele':markedPoint[2],
                                                    'time':markedTime,
                                                    'name':markedName,
                                                    'speed':0,
                                                    }]
                        coordinates = coordinates.append(markerWrite)
                    else:
                        coordinates.loc[
                        (coordinates.lat == markedPoint[1]) & 
                        (coordinates.lon == markedPoint[0]) & 
                        (coordinates.ele == markedPoint[2])
                        ,'name'] = markedName
            except:
                pass
            coordinates['time'] = pd.to_datetime(coordinates['time']).dt.time
            coordinates.sort_values('time',inplace=True)
            self.coordinates = coordinates

    def get_coordinates(self):
        return self.coordinates

    def get_json(self):
        return self.JSON

    def get_type(self):
        return self.type

    def set_info(self):
        import time

        def cal_time(ms):
            sec = int(ms)/1000
            minute = sec//60
            sec = sec%60
            hour = minute//60
            minute = minute%60
            day = hour//24
            hour = hour%240
            return [int(day),int(hour),int(minute),int(sec)]

        obj = self.JSON
        folder = obj['kml']['Document']['Folder']
        try:
            datafolder = folder[1]
        except:
            datafolder = folder
        self.documentation = obj['kml']['@xmlns']
        self.id = obj['kml']['Document']['@id']
        self.name = obj['kml']['Document']['name']
        self.description = datafolder['Placemark']['description']['div']
        self.snippet = obj['kml']['Document']['snippet']
        self.author = obj['kml']['Document']['author']
        for item in obj['kml']['Document']['ExtendedData']['Data']:
            if item['@name'] == 'TrackTags':
                self.TrackTags = item['value']
            if item['@name'] == 'BeginTime':
                self.BeginTime = time.localtime(int(str(item['value'])[:10]))
            if item['@name'] == 'EndTime':
                self.EndTime = time.localtime(int(str(item['value'])[:10]))
            if item['@name'] == 'TimeUsed':
                self.TimeUsed = cal_time(item['value'])
            if item['@name'] == 'PauseTime':
                self.TimePaused = cal_time(item['value'])
            if item['@name'] == 'PosStartName':
                self.PosStartName = item['value']
            if item['@name'] == 'PosEndName':
                self.PosEndName = item['value']
        [day_use,hour_use,minute_use,sec_use] = self.TimeUsed
        [day_pause,hour_pause,minute_pause,sec_pause] = self.TimePaused
        begintime = time.strftime('%Y-%m-%dT%H:%M:%SZ', self.BeginTime)
        self.begin = begintime
        begintime = f'Begin time: {begintime}.'
        endtime = time.strftime('%Y-%m-%dT%H:%M:%SZ', self.EndTime)
        self.end = endtime
        timeuse = f'Time used: {hour_use} hours(s), {minute_use} minute(s), {sec_use} second(s)'
        timepause = f'Time paused: {hour_pause} hours(s), {minute_pause} minute(s), {sec_pause} second(s)'
        self.use = timeuse
        self.pause = timepause

    def get_author(self):
        return self.author

    def get_trackType(self):
        return self.TrackTags

    def get_time(self):
        [day_use,hour_use,minute_use,sec_use] = self.TimeUsed
        [day_pause,hour_pause,minute_pause,sec_pause] = self.TimePaused
        begintime = time.strftime('%Y-%m-%dT%H:%M:%SZ', self.BeginTime)
        self.begin = begintime
        begintime = f'Begin time: {begintime}.'
        endtime = time.strftime('%Y-%m-%dT%H:%M:%SZ', self.EndTime)
        self.end = endtime
        endtime = f'End time: {endtime}.'
        timeuse = f'Time used: {hour_use} hours(s), {minute_use} minute(s), {sec_use} second(s).'
        timepause = f'Time paused: {hour_pause} hours(s), {minute_pause} minute(s), {sec_pause} second(s).'
        return ' '.join([begintime,endtime,timeuse,timepause])

    def get_loc(self):
        return f'start location: {self.PosStartName}, end location: {self.PosEndName}'

    def calculate_range(self):
        import math
        coordinates = self.coordinates
        (lonmin,latmin) = WGS84_to_WebM(coordinates.lon.min(),coordinates.lat.min())
        (lonmax,latmax) = WGS84_to_WebM(coordinates.lon.max(),coordinates.lat.max())
        lonrange = lonmax - lonmin
        latrange = latmax - latmin
        coordrange = max(lonrange,latrange)
        tilesize = int(math.log(40075014/coordrange,2))-1
        self.tilesize = tilesize

    def get_tilesize(self):
        return self.tilesize

    def get_customdata(self):
        if self.type == 'detailed':
            import numpy as np
            data = self.coordinates
            speesize = len(list(data.speed))
            spee = np.tile(np.array(data.speed),speesize)
            spee = np.reshape(spee, (speesize,speesize))
            spee = spee.T
            elee = np.tile(np.array(data.ele),speesize)
            elee = np.reshape(elee, (speesize,speesize))
            elee = elee.T
            return np.dstack((elee,spee))
        else:
            print("Input KML doesn't support this method.")

    def get_header(self):
        header=(f'### Track Author:  {self.author} <br> ' 
                f'###### Track Type: {self.TrackTags},{self.type}<br>' 
                f'------------------<br>' 
                f'Begin time: {self.begin}, start location: {self.PosStartName}, <br>' 
                f'<br>End time: {self.end}, end location: {self.PosEndName} <br>' 
                f'<br>Time used: {self.use}. <br>' 
                f'<br>Time paused: {self.pause}.')
        return header
        
    def set_colors(self):
        trackType = self.TrackTags
        coordinates = self.coordinates
        if trackType in ['爬山','徒步','散步']:
            maxspeed = 4
        elif trackType in ['跑步']:
            maxspeed = 10
        elif trackType in ['游泳']:
            maxspeed = 3
        elif trackType in ['骑行','滑雪']:
            maxspeed = 80
        elif trackType in ['轮滑']:
            maxspeed = 35
        elif trackType in ['摩托']:
            maxspeed = 350
        elif trackType in ['驾车']:
            maxspeed = 450
        elif trackType in ['轮船']:
            maxspeed = 55
        elif trackType in ['飞机']:
            maxspeed = 3600
        elif trackType in ['其他']:
            maxspeed = coordinates.speed.max()
        maxspeed = coordinates.speed.max()
        d = resize(coordinates.speed,maxspeed,0,100,0)
        return d

    def to_gpd(self):
        from shapely.geometry import Point
        import geopandas as gpd
        import pandas as pd
        coordinates = self.get_coordinates()
        gdf = gpd.GeoDataFrame(
            coordinates.drop(['lon', 'lat'], axis=1),
            crs={'init': 'epsg:4326'},
            geometry=[Point(xy) for xy in zip(coordinates.lon, coordinates.lat)])
        return gdf

    def write(self, filename, driverInfo, encodingInfo):
        import geopandas as gpd
        gdf = self.to_gpd()
        gpd.to_file(filename,driver=driverInfo,encoding=encodingInfo)

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