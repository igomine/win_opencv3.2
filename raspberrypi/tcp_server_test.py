import socket
import time
import sys

HOST_IP = "10.0.0.133"
HOST_PORT = 7654

# 创建Socket，SOCK_STREAM表示类型为TCP
print("Starting socket: TCP...")
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定IP和端口，并进行监听
# 137.58.230.162为本机IP，端口为7654
print("TCP server listen @ %s:%d!" % (HOST_IP, HOST_PORT))
host_addr = (HOST_IP, HOST_PORT)
socket_tcp.bind(host_addr)
socket_tcp.listen(1)

# 接受Client发出的连接请求，返回值包含了Client的IP和端口
socket_con, (client_ip, client_port) = socket_tcp.accept()
print("Connection accepted from %s." % client_ip)

data = "Welcome to RPi TCP server!"
# 向Clinet发送数据
socket_con.send(data.encode())

socket_tcp.close()
