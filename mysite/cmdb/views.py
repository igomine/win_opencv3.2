from django.shortcuts import render
from django.shortcuts import HttpResponse

from django.http import HttpResponse
from channels.handler import AsgiHandler

# Create your views here.


user_list = [
    {"user": "jack", "pwd": "abc"},
    {"user": "tom", "pwd": "ABC"},
]


def index(request):
    # return HttpResponse("hello chark")
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        temp = {"user": username, "pwd": password}
        user_list.append(temp)
    return render(request, "index.html", {"data": user_list} )


# 当连接上时，发回去一个connect字符串
def ws_connect(message):
    temp = {"user": "ws_connect", "pwd": "ws_connect"}
    user_list.append(temp)
    # message.reply_channel.send({"connect"})


# 将发来的信息原样返回
def ws_message(message):
    temp = {"user": "ws_message", "pwd": "ws_message"}
    user_list.append(temp)
    message.reply_channel.send({
        "text": message.content['text'],
    })


# 断开连接时发送一个disconnect字符串，当然，他已经收不到了
def ws_disconnect(message):
    temp = {"user": "ws_disconnect", "pwd": "ws_disconnect"}
    user_list.append(temp)
    message.reply_channel.send({"disconnect"})
