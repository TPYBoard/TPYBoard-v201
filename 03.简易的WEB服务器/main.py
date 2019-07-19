import pyb
from pyb import UART

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
html = """<!DOCTYPE html>
<html>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <head> <title>TPYBoard</title> </head>
    <body>
      <h1>TPYBoard v201</h1><br />
      <h2>Simple HTTP server</h2>
    </body>
</html>
"""

while True:
    if uart.any() > 0:
        request = uart.read().decode()
        print('request:',request)
        #当接收到GET请求头时，进行响应
        if request.find('GET') > -1:
            data = header.format(len(html),html)
            uart.write(data)