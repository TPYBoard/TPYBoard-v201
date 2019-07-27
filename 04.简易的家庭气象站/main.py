import pyb
from pyb import Timer,UART
from ds3231 import DS3231
from dht11 import DHT11

#串口6初始化
uart = UART(6,115200,timeout = 100)
#响应报文
header = """
HTTP/1.1 200 OK
Content-Type:text/html
Content-Length:{0}

{1}
"""
#HTML页面
html = """
<html>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <head> <title>TPYBoard v201</title> </head>
    <body>
        <h1>TPYBaord 家庭气象站</h1><br />
        <p>时间:{}</p>
        <p>温度:{}</p>
        <p>湿度:{}</p>
    </body>
</html>
"""

#------------------------DS3231----------------------------------#
ds=DS3231(2) #设置DS3231为I2C2接口,对应SCL-Y9,SDA-Y10
#初始日期和时间，设置一次即可
#ds.DATE([19,7,27])   #设置初始日期年、月、日
#ds.TIME([14,50,0])   #设置初始时间时、分、秒
#------------------------DHT11----------------------------------#
d = DHT11('X12')

def updateDisplay():

    DATE = [str(i) for i in ds.DATE()] #将返回的时间数据int转str
    TIME = [str(i) for i in ds.TIME()]
    time = '-'.join(DATE) + ' ' + ':'.join(TIME) #读取日期和时间，拼接成正常的时间格式
    data = d.read_data()             #读取温湿度的值
    return time,data

while True:
    if uart.any() > 0:
        request = uart.read().decode()
        print('request:',request)
        #当接收到GET请求头时，进行响应.同时把favicon.ico请求过滤掉
        if request.find('GET') > -1 and request.find('favicon.ico') < 0:
            time,data = updateDisplay()
            print(data)
            HTML = html.format(time,data[0],data[1])
            #print(HTML)
            uart.write(header.format(len(HTML),HTML))