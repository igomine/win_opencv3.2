import socket
import time
import sys

SERVER_IP = "10.0.0.133"
SERVER_PORT = 7654
# 创建Socket，SOCK_STREAM表示类型为TCP
print("Starting socket: TCP...")
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 向服务器发出连接请求，需要指定服务器IP和端口
print("Connecting to server @ %s:%d..." % (SERVER_IP, SERVER_PORT))
server_addr = (SERVER_IP, SERVER_PORT)
socket_tcp.connect(server_addr)

# 接收服务器发来的欢迎数据
data = socket_tcp.recv(512)
print("Server: %s" % data)

socket_tcp.close()
