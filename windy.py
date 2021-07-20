#access data through windy API 
def request(lon,lat):
    import requests
    import json
    post = {
        "lat": lat,
        "lon": lon,
        "model": "gfs",
        "parameters": ["temp", "wind", "precip", "rh", "pressure", "ptype", "lclouds", "mclouds", "hclouds", "windGust",],
        "levels": ["surface","1000h", "950h", '925h', "900h", '850h', '800h', '700h', '600h', '500h', '400h', '300h', "200h", "150h"],
        # "key": "dre0kCydf9Ce80uHxAYaQs2Vd2TCrBzV"
        "key":"voVizrMRe0hAw17zW4N4O4gkD885IenS"
        # "key": "lXIXVexIoMoYvQIjb1hoqAQmdXkLSRTb"
        # alternative 2 keys, for free API keys usage is limited.
        }
    r = requests.post('https://api.windy.com/api/point-forecast/v2', json = post)
    data = json.loads(r.text)
    return data

def getTimeSeriesVerticalWeather(JSON):
    import time
    ts = JSON['ts']
    hour=[]
    for i in range(len(ts)):
        hour.append(time.strftime("%Y-%m-%d-%Hh", time.localtime(int(str(ts[i])[:10]))))
    units = JSON['units']
    temp_units = units['temp-surface']
    uwind_units = units['wind_u-surface']
    vwind_units = units['wind_v-surface']
    past3hprecip_units = units['past3hprecip-surface']
    rh_units = units['rh-surface']
    pressure_units = units['pressure-surface']
    ptype_units = units['ptype-surface']
    clouds_units = units['lclouds-surface']
    gust_units = units['gust-surface']
    units = {'temp':temp_units,
                    'uwind':uwind_units,
                    'vwind':vwind_units,
                    'past3hprecip':past3hprecip_units,
                    'rh':rh_units,
                    'pressure':pressure_units,
                    'ptype':ptype_units,
                    'cloud':clouds_units,
                    'gust':gust_units
                    }
    temp_surface = JSON['temp-surface']
    temp_1000h = JSON['temp-1000h']
    temp_950h = JSON['temp-950h']
    temp_925h = JSON['temp-925h']
    temp_900h = JSON['temp-900h']
    temp_850h = JSON['temp-850h']
    temp_800h = JSON['temp-800h']
    temp_700h = JSON['temp-700h']
    temp_600h = JSON['temp-600h']
    temp_500h = JSON['temp-500h']
    temp_400h = JSON['temp-400h']
    temp_300h = JSON['temp-300h']
    temp_200h = JSON['temp-200h']
    temp_150h = JSON['temp-150h']
    temp = [temp_surface,temp_1000h,temp_950h,temp_925h,temp_900h,temp_850h,temp_800h,temp_700h,temp_600h,temp_500h,temp_400h,temp_300h,temp_200h,temp_150h]
    uwind_surface = JSON['wind_u-surface']
    uwind_1000h = JSON['wind_u-1000h']
    uwind_950h = JSON['wind_u-950h']
    uwind_925h = JSON['wind_u-925h']
    uwind_900h = JSON['wind_u-900h']
    uwind_850h = JSON['wind_u-850h']
    uwind_800h = JSON['wind_u-800h']
    uwind_700h = JSON['wind_u-700h']
    uwind_600h = JSON['wind_u-600h']
    uwind_500h = JSON['wind_u-500h']
    uwind_400h = JSON['wind_u-400h']
    uwind_300h = JSON['wind_u-300h']
    uwind_200h = JSON['wind_u-200h']
    uwind_150h = JSON['wind_u-150h']
    uwind = [uwind_surface,uwind_1000h,uwind_950h,uwind_925h,uwind_900h,uwind_850h,uwind_800h,uwind_700h,uwind_600h,uwind_500h,uwind_400h,uwind_300h,uwind_200h,uwind_150h]
    vwind_surface = JSON['wind_v-surface']
    vwind_1000h = JSON['wind_v-1000h']
    vwind_950h = JSON['wind_v-950h']
    vwind_925h = JSON['wind_v-925h']
    vwind_900h = JSON['wind_v-900h']
    vwind_850h = JSON['wind_v-850h']
    vwind_800h = JSON['wind_v-800h']
    vwind_700h = JSON['wind_v-700h']
    vwind_600h = JSON['wind_v-600h']
    vwind_500h = JSON['wind_v-500h']
    vwind_400h = JSON['wind_v-400h']
    vwind_300h = JSON['wind_v-300h']
    vwind_200h = JSON['wind_v-200h']
    vwind_150h = JSON['wind_v-150h']
    vwind = [vwind_surface,vwind_1000h,vwind_950h,vwind_925h,vwind_900h,vwind_850h,vwind_800h,vwind_700h,vwind_600h,vwind_500h,vwind_400h,vwind_300h,vwind_200h,vwind_150h]
    past3hprecip_surface = JSON['past3hprecip-surface']
    rh_surface = JSON['rh-surface']
    rh_1000h = JSON['rh-1000h']
    rh_950h = JSON['rh-950h']
    rh_925h = JSON['rh-925h']
    rh_900h = JSON['rh-900h']
    rh_850h = JSON['rh-850h']
    rh_800h = JSON['rh-800h']
    rh_700h = JSON['rh-700h']
    rh_600h = JSON['rh-600h']
    rh_500h = JSON['rh-500h']
    rh_400h = JSON['rh-400h']
    rh_300h = JSON['rh-300h']
    rh_200h = JSON['rh-200h']
    rh_150h = JSON['rh-150h']
    rh = [rh_surface,rh_1000h,rh_950h,rh_925h,rh_900h,rh_850h,rh_800h,rh_700h,rh_600h,rh_500h,rh_400h,rh_300h,rh_200h,rh_150h]
    pressure_surface = JSON['pressure-surface']
    ptype_surface = JSON['ptype-surface']
    lclouds_surface = JSON['lclouds-surface']
    mclouds_surface = JSON['mclouds-surface']
    hclouds_surface = JSON['hclouds-surface']
    cloud = [lclouds_surface,mclouds_surface,hclouds_surface]
    gust_surface = JSON['gust-surface']
    pressure = [0,1000,950,925,900,850,800,700,600,500,400,300,200,150]
    verticalInfo = [hour, pressure, temp, uwind, vwind, rh, cloud, pressure_surface, ptype_surface, past3hprecip_surface, gust_surface]
    return units,verticalInfo

def getCertainTimeVerticalWeather(iodata, timePoint):
    # timePoint (int): (you can use getNumberOfData(verticalInfo, timeStr) function to find index)the Index of the time you want to get the detailed weather information
    # return type: (array): [timeStr, pressure, temp, uwind, vwind, rh, cloud, pressure_surface, ptype_surface, past3hprecip_surface, gust_surface]
    if timePoint < len(iodata[0]) and timePoint >= 0:
        timeStr = iodata[0][timePoint]
        pressure = iodata[1]
        temp = [] 
        uwind = [] 
        vwind = [] 
        rh = [] 
        cloud = [] 
        pressure_surface = [] 
        ptype_surface = [] 
        past3hprecip_surface = [] 
        gust_surface = []

        for j in range(len(iodata[1])):
            temp.append(iodata[2][j][timePoint]) 
            uwind.append(iodata[3][j][timePoint]) 
            vwind.append(iodata[4][j][timePoint]) 
            rh.append(iodata[5][j][timePoint]) 
        for j in range(len(iodata[6])):
            cloud.append(iodata[6][j][timePoint])      
        pressure_surface.append(iodata[7][timePoint]) 
        ptype_surface.append(iodata[8][timePoint])
        past3hprecip_surface.append(iodata[9][timePoint]) 
        gust_surface.append(iodata[10][timePoint])
            
        return [timeStr, pressure, temp, uwind, vwind, rh, cloud, pressure_surface, ptype_surface, past3hprecip_surface, gust_surface]
    else:
        return ('Requested time point is out of forecast period, please check.')   

def getSurfaceWeather(iodata):
    [timeStr, pressure, temp, uwind, vwind, rh, cloud, pressure_surface, ptype_surface, past3hprecip_surface, gust_surface] = iodata
    temp_surface = temp[0]
    uwind_surface = uwind[0]
    vwind_surface = vwind[0]
    rh_surface = rh[0]
    lclouds_surface = cloud[0]
    mclouds_surface = cloud[1]
    hclouds_surface = cloud[2]
    return [timeStr, temp_surface, uwind_surface, vwind_surface, rh_surface,lclouds_surface, mclouds_surface,hclouds_surface, pressure_surface, ptype_surface, past3hprecip_surface, gust_surface]

def getSurfaceForecast(surfaceIodata):
    import pandas as pd
    import numpy as np
    surface = pd.DataFrame(surfaceIodata)
    surface = surface.T
    surface.columns = ['time', 'temp_surface', 'uwind_surface', 'vwind_surface', 'rh_surface','lclouds_surface', 'mclouds_surface','hclouds_surface', 'pressure_surface', 'ptype_surface', 'past3hprecip_surface', 'gust_surface']
    def pd_round(inputSeries):
        pdd=pd.DataFrame(inputSeries)
        pdd=pdd.round(1)
        pdd=pd.Series(pdd.iloc[:,0])
        pdd=pdd.astype(int)
        return pdd
    surface['time'] = pd.to_datetime(surface['time'])
    forecast=pd.DataFrame(surface.time)
    forecast['temp_surface'] = surface['temp_surface'] - 273.15
    forecast['temp_surface'] = np.round(list(forecast['temp_surface']),decimals=1)
    forecast['precipation3h'] = surface['past3hprecip_surface']
    forecast['lclouds_show'] = pd_round(surface['lclouds_surface']/10)
    forecast['lclouds_surface'] = pd_round(surface['lclouds_surface'])
    forecast['mclouds_show'] = pd_round(surface['mclouds_surface']/10)
    forecast['mclouds_surface'] = pd_round(surface['mclouds_surface'])
    forecast['hclouds_show'] = pd_round(surface['hclouds_surface']/10)
    forecast['hclouds_surface'] = pd_round(surface['hclouds_surface'])
    forecast['wind_surface'] = np.sqrt(
        list(surface['uwind_surface']**2 + surface['vwind_surface']**2)
        )
    forecast['wind_surface'] = np.round(list(forecast['wind_surface']),decimals=1)
    forecast['gust_surface'] = np.round(list(surface['gust_surface']),decimals=1)
    forecast['rh_surface'] = pd_round(surface['rh_surface'])
    forecast['wind_aspect'] = pd_round(
        np.arctan2(
            list(surface['vwind_surface']),
            list(surface['uwind_surface'])
            )* 180 / np.pi
            )
    forecast['wind_asp']='W'
    forecast.loc[
        (forecast['wind_aspect'] == 0) |
        (forecast['wind_aspect'] == 360)
    ,'wind_asp'] = 'E'
    forecast.loc[
        (forecast['wind_aspect'] == -90)
    ,'wind_asp'] = 'S'
    forecast.loc[
        (forecast['wind_aspect'] == 180) |
        (forecast['wind_aspect'] == -180)
    ,'wind_asp'] = 'W'
    forecast.loc[
        (forecast['wind_aspect'] == 90)
    ,'wind_asp'] = 'N'
    forecast.loc[
        (forecast['wind_aspect'] > 0) &
        (forecast['wind_aspect'] < 90)
    ,'wind_asp'] = 'NE'
    forecast.loc[
        (forecast['wind_aspect'] > 90) &
        (forecast['wind_aspect'] < 180)
    ,'wind_asp'] = 'NW'
    forecast.loc[
        (forecast['wind_aspect'] > -90) &
        (forecast['wind_aspect'] < 0)
    ,'wind_asp'] = 'SE'
    forecast.loc[
        (forecast['wind_aspect'] > -180) &
        (forecast['wind_aspect'] < -90)
    ,'wind_asp'] = 'SW'
    forecast.wind_aspect = forecast['wind_asp']
    forecast['weather'] = ''
    forecast['clouds_show'] = forecast['lclouds_show']
    forecast.loc[
        (forecast['mclouds_show'] > forecast['lclouds_show']) &
        (forecast['mclouds_show'] > forecast['hclouds_show'])
    ,'clouds_show'] = list(forecast.mclouds_show[
        (forecast['mclouds_show'] > forecast['lclouds_show']) &
        (forecast['mclouds_show'] > forecast['hclouds_show'])
    ])
    forecast.loc[
        (forecast['hclouds_show'] > forecast['lclouds_show']) &
        (forecast['hclouds_show'] > forecast['mclouds_show'])
    ,'clouds_show'] = list(forecast.hclouds_show[
        (forecast['hclouds_show'] > forecast['lclouds_show']) &
        (forecast['hclouds_show'] > forecast['mclouds_show'])
    ])
    forecast.loc[
        (surface['ptype_surface'] == 0) & 
        (forecast['clouds_show'] < 2)
        ,'weather'] = '晴'
    forecast.loc[
        (surface['ptype_surface'] == 0) & 
        (forecast['clouds_show'] >= 8)
        ,'weather'] = '阴' # 参考资料: http://www.kepu.net.cn/gb/earth/weather/water/wtr010.html
    forecast.loc[
        (surface['ptype_surface'] == 0) & 
        (forecast['clouds_show'] >= 1) &
        (forecast['clouds_show'] <= 3)
        ,'weather'] = '少云' #  10%至30%称为少云
    forecast.loc[
        (surface['ptype_surface'] == 0) & 
        (forecast['clouds_show'] >= 4) &
        (forecast['clouds_show'] <= 7) 
        ,'weather'] = '多云' # 30%至70%称为多云
    forecast.loc[
        (surface['ptype_surface'] == 1)
    ,'weather'] = '雨'
    forecast.loc[
        (surface['ptype_surface'] == 5)
    ,'weather'] = '雪'
    forecast.loc[
        (surface['ptype_surface'] == 6)
    ,'weather'] = '湿雪'
    forecast = forecast.drop(['mclouds_show', 'lclouds_show', 'hclouds_show', 'clouds_show', 'wind_asp'], axis=1)
    return forecast  
    
def getNumberOfData(verticalInfo, timeStr):
    for i in range(0, len(verticalInfo[0])):
        if verticalInfo[0][i].find(timeStr) != -1:
            return i
    return -1
