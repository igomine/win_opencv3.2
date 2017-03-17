from channels.routing import route
from mysite import consumer  #导入处理函数
from cmdb import views

channel_routing = [
    #route("http.request", consumers.http_consumer), 这个表项比较特殊，他响应的是http.request，也就是说有HTTP请求时就会响应，同时urls.py里面的表单会失效


    # route("websocket.connect", views.ws_connect),        #当WebSocket请求连接上时调用consumers.ws_connect函数
    route("websocket.receive", views.ws_message),        #当WebSocket请求发来消息时。。。
    route("websocket.disconnect", views.ws_disconnect),    #当WebSocket请求断开连接时。。。
]