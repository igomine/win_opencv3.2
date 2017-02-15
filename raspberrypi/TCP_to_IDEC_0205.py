import socket
import time
import sys
import struct

IDEC_COMMAND_WRITE_DO_4BYTE = [0, 0, 0, 0, 0, 0x0B, 1, 0x0F, 0, 0, 0, 0x20, 4, 0, 0, 0, 0]
IDEC_RETURN_WRITE_DO = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

IDEC_COMMAND_READ_DI_40CHNEL = [0, 0, 0, 0, 0, 6, 1, 2, 0, 0, 0, 0x28]
IDEC_RETURN_READ_DI = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

SERVER_IP = "192.168.1.104"
SERVER_PORT = 7654

for d in range(1, 10):
    print("%x" % d, end=" ")

print("Starting socket: TCP...")
server_addr = (SERVER_IP, SERVER_PORT)
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        print("Connecting to server @ %s:%d..." % (SERVER_IP, SERVER_PORT))
        socket_tcp.connect(server_addr)
        break
    except Exception:
        print("Can't connect to server, try it latter!")
        time.sleep(1)
        continue
for test in range(10, 20):
    print('%x' % test, end=" ")
print("DO output")
print("祝各位身体健康", end=' ')
print("！")

while True:
    try:
        send_date = struct.pack("%dB" % (len(IDEC_COMMAND_WRITE_DO_4BYTE)), *IDEC_COMMAND_WRITE_DO_4BYTE)
        socket_tcp.send(send_date)
        rcv_data = socket_tcp.recv(512)
        if len(rcv_data) > 0:
            # unpack_rcv_data = struct.unpack("%dB" % len(rcv_data), rcv_data)
            for i in rcv_data:
                print("3")
                print("0x%x" % i, end=" ")
        # time.sleep(1)
        continue
    except Exception:
        print("error:tcp closed")
        socket_tcp.close()
        socket_tcp = None
        sys.exit(1)
