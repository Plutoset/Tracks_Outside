# Tracks Outside Documendation
kml格式是常见的记录户外轨迹的方式。在野外实习中常用的两步路户外助手软件中，可以轻松记录轨迹，然而，其kml格式并不规范。

在野外科考或者外出旅游的过程中，大家往往会参考已有的他人的路线，结合天气预报等参数，对于自己的出行进行分析。
### 实现功能：
- 本产品基于Dash, Plotly, Flask, GeoPandas等库，建立了新的类kml存储kml数据，并且可以导出为shapefile进行下一步分析。
- 使用了Windy的Point Weather Forecast API，实现输入坐标，获得该点的近地表和多气压层的天气预报数据并且进行可视化。
- 使用Dash提供的Web框架，实现了基本Web页面搭建。
### 依赖库: 
依赖|   |   |
---|---|---|
dash    |plotly |flask      |
pandas  |numpy  |xmltodict  |
base64  |xlrd   |requests   |
joblib  |xlwt   |io         |
### 程序页面：
![header](https://github.com/Plutoset/Tracks_Outside/blob/master/figures/header.png?raw=true "header")

![kmlinfo](https://github.com/Plutoset/Tracks_Outside/blob/master/figures/kmlinfo.png?raw=true "kmlinfo")

![kmlmap](https://github.com/Plutoset/Tracks_Outside/blob/master/figures/kmlmap.png?raw=true "kmlmap")

![forecast](https://github.com/Plutoset/Tracks_Outside/blob/master/figures/forecast.png?raw=true "forecast")

### kml类结构和函数
> __init__(self, Input):
>> Input: 一串指向kml路径的字符串，或者数据流。

> get_coordinates(self):
>> 返回一个包括kml中所有轨迹点数据的DataFrame，column中包含：lon, lat, ele, speed(optional), time(optional)

> get_json(self):
>> 返回json格式的kml原始数据。

> get_type(self):
>> 返回此kml的类别，raw格式（点数据中不包含速度和时间）或者detailed格式（点数据中包括了速度和时间）

> get_author(self):
>> 返回轨迹作者

> get_trackType(self):
>> 返回轨迹类型（徒步，跑步，骑车，游泳等）

> get_time(self):
>> 返回一个字符串，包括了开始时间，结束时间，运动时长，休息时间

> get_loc(self):
>> 返回一个字符串，包括了起点和终点的名字

> get_tilesize(self):
>> 返回轨迹大小所对应的切片地图尺寸

> get_customdata(self):
>> 返回切片地图可视化的数据

> get_header(self):
>> 返回轨迹的header信息，包括了作者，起始和终止时间和地理位置，运动时间和休息时间。

> set_colors(self):
>> 返回切片地图可视化的色彩分类等级数据

> to_gpd(self):
>> 返回GeoPandas格式的数据

> write(self, filename, driverInfo, encodingInfo):
>> 将轨迹写入Shapefile文件。

### Windy API使用
**[Windy官网](https://www.windy.com/)需要通过国外VPN访问**

> request(lon,lat):
>> 返回json格式的天气预报数据

> getTimeSeriesVerticalWeather(JSON):
>> 输入json格式的天气预报数据
>> 返回数据单位列表和垂直数据列表，列表中的数据分别为时间，气压（两个尺度），温度，径向风，纬向风，湿度，云量（只有低，中，高云），地表气压（无垂直尺度），地表降水类型（无垂直尺度），地表降水量（无垂直尺度），地表疾风（无垂直尺度）

> getCertainTimeVerticalWeather(iodata, timePoint):
>> 输入垂直数据和想要获取的时间切片序列名
>> 返回该时间上的天气预报值，包括时间，气压（有垂直尺度），温度（有垂直尺度），径向风（有垂直尺度），纬向风（有垂直尺度），湿度（有垂直尺度），云量，地表气压，地表降水类型，地表降水量，地表疾风

> getSurfaceWeather(iodata):
>> 输入垂直数据
>> 返回地表气象预报列表，包括时间，地表气温，地表径向风，地表纬向风，地表湿度，地表低云量，地表中云量，地表高云量，地表气压，地表降水类型，地表降水量，地表疾风

> getSurfaceForecast(surfaceIodata):
>> 计算地表气象预报，返回DataFrame

> getNumberOfData(verticalInfo, timeStr):
>> 输入时间字符串，计算该时间字符串是否位于天气预报的时间范围内

> show_forecast(forecast):
>> 返回预报可视化结果

> forecast_all(lon,lat):
>> 整合Windy API中的所有步骤

> plot_kml(k, originalfig):
>> 输入需要可视化的kml文件和原始图像
>> 返回叠加了可视化的kml轨迹后的图像

-------------------
因为时间所限（我们于7月10日出发前往新疆参与实习），有部分功能因为时间所限未能完成。接下来的程序会在[我的GitHub库](https://github.com/Plutoset/Tracks_Outside)持续更新。
### 预计实现功能：
- 在Web页面实现支持文件下载
- 在Web页面实现切片地图底图切换
- 在Web页面实现数据编辑
